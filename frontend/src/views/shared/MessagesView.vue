<script setup lang="ts">
import { onMounted, ref, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useMessageStore } from '../../stores/messageStore';
import { useAuthStore } from '../../stores/authStore';
import { computed } from 'vue';
import api from '../../services/api';

const route = useRoute();
const messageStore = useMessageStore();
const authStore = useAuthStore();

const newMessage = ref('');
const messagesDropdown = ref<HTMLElement | null>(null);

const pendingReceiverId = ref<number | null>(null);
const pendingShopName = ref<string | null>(null);

const showDeleteConfirm = ref(false);
const conversationToDelete = ref<any>(null);

// Mobile panel state: 'list' | 'chat'
const mobilePanel = ref<'list' | 'chat'>('list');

onMounted(async () => {
  await messageStore.fetchConversations();
  if (authStore.user) {
    messageStore.connectWS(authStore.user.id);
  }

  const providerId = route.query.provider_id ? Number(route.query.provider_id) : null;
  const receiverId = route.query.receiver_id ? Number(route.query.receiver_id) : null;
  const shopName = route.query.shop_name as string;
  const customerName = route.query.customer_name as string;

  if (providerId) {
    const existing = messageStore.conversations.find(c => c.provider_id === providerId);
    if (existing) {
      selectConversation(existing.id);
    } else if (receiverId) {
      messageStore.activeConversationId = -1;
      messageStore.activeMessages = [];
      pendingReceiverId.value = receiverId;
      pendingShopName.value = shopName || `Provider #${providerId}`;
      mobilePanel.value = 'chat';
    }
  } else if (receiverId) {
    const existing = messageStore.conversations.find(c => c.user_id === receiverId);
    if (existing) {
      selectConversation(existing.id);
    } else {
  
      messageStore.activeConversationId = -1;
      messageStore.activeMessages = [];
      pendingReceiverId.value = receiverId;
      pendingShopName.value = customerName || `User #${receiverId}`;
      mobilePanel.value = 'chat';
    }
  }
});

const selectConversation = async (id: number) => {
  pendingReceiverId.value = null;
  pendingShopName.value = null;
  await messageStore.fetchMessages(id);
  await messageStore.markAsRead(id);
  mobilePanel.value = 'chat';
  scrollToBottom();
};

const goBackToList = () => {
  mobilePanel.value = 'list';
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  let targetReceiverId: number | null = null;

  if (messageStore.activeConversationId === -1 && pendingReceiverId.value) {
    targetReceiverId = pendingReceiverId.value;
  } else if (messageStore.activeConversationId) {
    const conv = messageStore.conversations.find(c => c.id === messageStore.activeConversationId);
    if (conv) {
      
      targetReceiverId = authStore.user.id === conv.user_id 
        ? conv.provider_owner_id 
        : conv.user_id;
    }
  }

  if (!targetReceiverId) {
    console.error("Could not determine recipient ID", {
      activeId: messageStore.activeConversationId,
      pendingId: pendingReceiverId.value,
      conv: messageStore.conversations.find(c => c.id === messageStore.activeConversationId)
    });
    return;
  }

  try {
    const msg = await messageStore.send(targetReceiverId, newMessage.value);
    newMessage.value = '';
    
    if (messageStore.activeConversationId === -1) {
       messageStore.activeConversationId = msg.conversation_id;
       pendingReceiverId.value = null;
       pendingShopName.value = null;
       await messageStore.fetchConversations();
    }
    
    scrollToBottom();
  } catch (err) {
    console.error("Failed to send message", err);
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesDropdown.value) {
      messagesDropdown.value.scrollTop = messagesDropdown.value.scrollHeight;
    }
  });
};

const confirmDelete = (conv: any) => {
  conversationToDelete.value = conv;
  showDeleteConfirm.value = true;
};

const handleDelete = async () => {
  if (!conversationToDelete.value) return;
  try {
    await messageStore.deleteConversation(conversationToDelete.value.id);
    showDeleteConfirm.value = false;
    conversationToDelete.value = null;
  } catch (err) {
    alert("Failed to delete conversation");
  }
};

watch(() => messageStore.activeMessages.length, () => {
  scrollToBottom();
});

const formatTime = (iso: string) => {
  if (!iso) return '';
  
  const dateStr = iso.includes('T') ? iso : iso.replace(' ', 'T');
  return new Date(dateStr).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  });
};

const getDisplayName = (conv: any) => {
  
    if (!authStore.user) return '';
    if (authStore.user.id === conv.user_id) {
        return conv.shop_name;
    }
    return conv.user_name;
};

const imgUrl = (path: string) => {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}`;
};

const activeConversation = computed(() => {
  if (!messageStore.activeConversationId) return null;
  if (messageStore.activeConversationId === -1) return null;
  return messageStore.conversations.find(c => c.id === messageStore.activeConversationId) || null;
});
</script>

<template>
  <div class="page" :data-panel="mobilePanel">
    <div class="page-header">
      <h1 class="title">Messages</h1>
      <p class="hint">Keep in touch with your service providers and clients.</p>
    </div>

    <div class="chat-container">
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="conversation-list">
          <div 
            v-for="conv in messageStore.conversations" 
            :key="conv.id"
            class="conversation-item"
            :class="{ active: conv.id === messageStore.activeConversationId }"
            @click="selectConversation(conv.id)"
          >
            <div class="avatar profile-img" v-if="authStore.user?.id === conv.user_id && conv.provider_profile_image">
               <img :src="imgUrl(conv.provider_profile_image)" alt="Profile" />
            </div>
            <div class="avatar profile-img" v-else-if="authStore.user?.id !== conv.user_id && conv.user_profile_image">
               <img :src="imgUrl(conv.user_profile_image)" alt="Profile" />
            </div>
            <div class="avatar" v-else>
              {{ getDisplayName(conv).charAt(0) }}
            </div>
            <div class="conv-info">
              <div class="conv-top">
                <span class="name">{{ getDisplayName(conv) }}</span>
                <span class="time">{{ formatTime(conv.updated_at) }}</span>
              </div>
              <p class="last-msg">{{ conv.last_message || 'No messages yet' }}</p>
            </div>
            <button class="delete-btn" @click.stop="confirmDelete(conv)" title="Delete Conversation">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          </div>
          
          <div v-if="messageStore.conversations.length === 0" class="empty-state">
             <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
               <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
             </svg>
            <p>No conversations yet</p>
          </div>
        </div>
      </div>

      <!-- Chat Window -->
      <div class="chat-window">
        <template v-if="messageStore.activeConversationId">
          <div class="chat-header">
            <!-- Mobile back button -->
            <button class="back-btn" @click="goBackToList" aria-label="Back to conversations">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 5l-7 7 7 7" />
              </svg>
            </button>
            <div class="header-info">
              <template v-if="messageStore.activeConversationId === -1">
                <div class="avatar sm">{{ pendingShopName?.charAt(0) }}</div>
                <div class="header-details">
                  <h3>{{ pendingShopName }}</h3>
                  <span class="status-tag">New Chat</span>
                </div>
              </template>
              <template v-else-if="activeConversation">
                <div class="avatar sm profile-img" v-if="authStore.user?.id === activeConversation.user_id && activeConversation.provider_profile_image">
                   <img :src="imgUrl(activeConversation.provider_profile_image)" alt="Profile" />
                </div>
                <div class="avatar sm profile-img" v-else-if="authStore.user?.id !== activeConversation.user_id && activeConversation.user_profile_image">
                   <img :src="imgUrl(activeConversation.user_profile_image)" alt="Profile" />
                </div>
                <div class="avatar sm" v-else>
                  {{ getDisplayName(activeConversation).charAt(0) }}
                </div>
                <div class="header-details">
                  <h3>{{ getDisplayName(activeConversation) }}</h3>
                  <router-link 
                    v-if="authStore.user?.id === activeConversation.user_id"
                    :to="`/providers/${activeConversation.provider_id}`" 
                    class="view-profile-btn"
                  >
                    View Profile
                  </router-link>
                </div>
              </template>
            </div>
          </div>

          <div class="messages-area" ref="messagesDropdown">
            <div 
              v-for="msg in messageStore.activeMessages" 
              :key="msg.id"
              class="message-wrapper"
              :class="{ 'mine': msg.sender_id === authStore.user?.id }"
            >
              <div class="message-bubble">
                <p>{{ msg.content }}</p>
                <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="chat-footer">
            <div class="input-wrapper">
              <input 
                v-model="newMessage" 
               @keydown.enter.prevent="sendMessage"
                placeholder="Type a message..."
              />
              <button @click="sendMessage" :disabled="!newMessage.trim()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        </template>
        
        <div v-else class="chat-empty">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <h3>Select a conversation to start chatting</h3>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay">
      <div class="modal-card">
        <h3>Delete Conversation</h3>
        <p>Do you want to delete your conversation with <strong>{{ getDisplayName(conversationToDelete) }}</strong>?</p>
        <p class="warning-text">This action is permanent and will delete the chat for both of you.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showDeleteConfirm = false">Cancel</button>
          <button class="btn-delete" @click="handleDelete">Delete Forever</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "../../styles/shared/MessagesView.css";
</style>
