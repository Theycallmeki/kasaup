<script setup lang="ts">
import { onMounted, ref, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useMessageStore } from '../stores/messageStore';
import { useAuthStore } from '../stores/authStore';
import { computed } from 'vue';
import api from '../services/api';

const route = useRoute();
const messageStore = useMessageStore();
const authStore = useAuthStore();

const newMessage = ref('');
const messagesDropdown = ref<HTMLElement | null>(null);

const pendingReceiverId = ref<number | null>(null);
const pendingShopName = ref<string | null>(null);

const showDeleteConfirm = ref(false);
const conversationToDelete = ref<any>(null);

onMounted(async () => {
  await messageStore.fetchConversations();
  if (authStore.user) {
    messageStore.connectWS(authStore.user.id);
  }

  // Handle auto-selecting or starting a chat with a specific provider
  const providerId = route.query.provider_id ? Number(route.query.provider_id) : null;
  const receiverId = route.query.receiver_id ? Number(route.query.receiver_id) : null;
  const shopName = route.query.shop_name as string;

  if (providerId) {
    const existing = messageStore.conversations.find(c => c.provider_id === providerId);
    if (existing) {
      selectConversation(existing.id);
    } else if (receiverId) {
      // New chat state
      messageStore.activeConversationId = -1;
      messageStore.activeMessages = [];
      pendingReceiverId.value = receiverId;
      pendingShopName.value = shopName || `Provider #${providerId}`;
    }
  }
});

const selectConversation = async (id: number) => {
  pendingReceiverId.value = null;
  pendingShopName.value = null;
  await messageStore.fetchMessages(id);
  scrollToBottom();
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  let targetReceiverId: number | null = null;

  if (messageStore.activeConversationId === -1 && pendingReceiverId.value) {
    targetReceiverId = pendingReceiverId.value;
  } else if (messageStore.activeConversationId) {
    const conv = messageStore.conversations.find(c => c.id === messageStore.activeConversationId);
    if (conv) {
      // If current user is the customer (user_id), send to provider owner.
      // If current user is the provider owner, send to the customer (user_id).
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
    
    // If it was a new conversation, update the active state
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
  // The backend now sends PHT (Philippines Time) directly.
  // We just need to ensure the format is valid for the Date constructor.
  const dateStr = iso.includes('T') ? iso : iso.replace(' ', 'T');
  return new Date(dateStr).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  });
};

const getDisplayName = (conv: any) => {
    // If I am the user (customer), show the shop name.
    // If I am the provider owner, show the user (customer) name.
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
  <div class="page">
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
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  height: 100vh;
  padding: 36px 32px;
  background: #0e0c1a;
  display: flex;
  flex-direction: column;
  font-family: 'DM Sans', sans-serif;
}

.page-header {
  margin-bottom: 24px;
  flex-shrink: 0;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}

.chat-container {
  flex: 1;
  min-height: 0;
  display: flex;
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

.sidebar {
  width: 320px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #a78bfa rgba(255,255,255,0.05);
  padding-right: 2px;
}

.conversation-list::-webkit-scrollbar {
  width: 5px;
}
.conversation-list::-webkit-scrollbar-track {
  background: transparent;
}
.conversation-list::-webkit-scrollbar-thumb {
  background: rgba(167, 139, 250, 0.15);
  border-radius: 10px;
}
.conversation-list::-webkit-scrollbar-thumb:hover {
  background: rgba(167, 139, 250, 0.3);
}

.conversation-item {
  padding: 18px 20px;
  display: flex;
  gap: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.conversation-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.conversation-item.active {
  background: rgba(167, 139, 250, 0.1);
  border-right: 3px solid #a78bfa;
}

.delete-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(248, 113, 113, 0.1);
  color: rgba(248, 113, 113, 0.5);
  border: 0.5px solid rgba(248, 113, 113, 0.2);
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  align-self: center;
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background: #f87171;
  color: #fff;
  border-color: #f87171;
  transform: scale(1.1);
}

.avatar {
  width: 50px;
  height: 50px;
  background: rgba(167, 139, 250, 0.15);
  border: 1px solid rgba(167, 139, 250, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c4b5fd;
  font-weight: 700;
  font-family: 'Sora', sans-serif;
  flex-shrink: 0;
  overflow: hidden;
}

.avatar.sm {
  width: 36px;
  height: 36px;
  font-size: 14px;
}

.profile-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.conv-info {
  flex: 1;
  min-width: 0;
}

.conv-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.name {
  font-weight: 500;
  color: #fff;
  font-size: 15px;
}

.time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.3);
}

.last-msg {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.015);
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.1);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-details h3 {
  margin: 0;
  font-size: 16px;
  font-family: 'Sora', sans-serif;
  color: #fff;
}

.status-tag {
  font-size: 10px;
  color: #a78bfa;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  margin-top: 2px;
  display: block;
}

.view-profile-btn {
  font-size: 12px;
  color: #a78bfa;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.view-profile-btn:hover {
  text-decoration: underline;
  opacity: 0.8;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scrollbar-width: thin;
  scrollbar-color: #a78bfa rgba(255,255,255,0.02);
}

.messages-area::-webkit-scrollbar {
  width: 6px;
}
.messages-area::-webkit-scrollbar-track {
  background: transparent;
}
.messages-area::-webkit-scrollbar-thumb {
  background: rgba(167, 139, 250, 0.1);
  border-radius: 10px;
  border: 1px solid transparent;
}
.messages-area::-webkit-scrollbar-thumb:hover {
  background: rgba(167, 139, 250, 0.25);
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 80%;
  align-self: flex-start;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #fff;
  line-height: 1.5;
}

.message-bubble p {
  margin: 0;
  font-size: 14px;
}

.msg-time {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.3);
  margin-top: 6px;
  display: block;
}

.mine {
  align-self: flex-end;
}

.mine .message-bubble {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: none;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.mine .msg-time {
  color: rgba(255, 255, 255, 0.6);
  text-align: right;
}

.chat-footer {
  padding: 20px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.input-wrapper {
  display: flex;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  padding: 8px 8px 8px 18px;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s;
}

.input-wrapper:focus-within {
  border-color: #a78bfa;
  background: rgba(255, 255, 255, 0.07);
}

.input-wrapper input {
  flex: 1;
  background: none;
  border: none;
  color: #fff;
  font-size: 14px;
  font-family: inherit;
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.2);
}

.input-wrapper input:focus {
  outline: none;
}

.input-wrapper button {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, opacity 0.2s;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.input-wrapper button:hover:not(:disabled) {
  transform: translateY(-1px);
  opacity: 0.9;
}

.input-wrapper button:active {
  transform: translateY(0);
}

.input-wrapper button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.2);
  text-align: center;
}

.empty-icon {
  margin-bottom: 24px;
  opacity: 0.1;
  transform: scale(1.5);
}

.chat-empty h3 {
  font-weight: 500;
  font-size: 1.1rem;
  font-family: 'Sora', sans-serif;
  letter-spacing: 0.02em;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 30px;
  text-align: center;
  color: rgba(255, 255, 255, 0.15);
  gap: 12px;
}

.empty-state p {
  font-size: 14px;
  margin: 0;
}

/* Confirmation Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-card {
  background: #1c1c24;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5);
  text-align: center;
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-card h3 {
  font-family: 'Sora', sans-serif;
  color: #fff;
  margin: 0 0 16px;
}

.modal-card p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
  margin-bottom: 20px;
}

.warning-text {
  color: #f87171 !important;
  font-weight: 500;
  font-size: 13px !important;
}

.modal-actions {
  display: flex;
  gap: 12px;
}

.modal-actions button {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.1);
}

.btn-delete {
  background: #f87171;
  color: #fff;
}

.btn-delete:hover {
  background: #ef4444;
  transform: translateY(-1px);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 900px) {
    .sidebar {
        width: 80px;
        min-width: 80px;
    }
    .conv-info {
        display: none;
    }
    .avatar {
        margin: 0 auto;
    }
    .conversation-item {
        padding: 15px 0;
        justify-content: center;
    }
}

@media (max-width: 640px) {
  .page {
    padding: 20px 14px;
  }
}
</style>
