<script setup lang="ts">
import { onMounted, ref, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useMessageStore } from '../stores/messageStore';
import { useAuthStore } from '../stores/authStore';

const route = useRoute();
const messageStore = useMessageStore();
const authStore = useAuthStore();

const newMessage = ref('');
const messagesDropdown = ref<HTMLElement | null>(null);

const pendingReceiverId = ref<number | null>(null);
const pendingShopName = ref<string | null>(null);

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
      targetReceiverId = authStore.user.id === conv.user_id ? conv.provider_id : conv.user_id;
    }
  }

  if (!targetReceiverId) return;

  try {
    const msg = await messageStore.send(targetReceiverId, newMessage.value);
    newMessage.value = '';
    
    // If it was a new conversation, we might need to select it
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

watch(() => messageStore.activeMessages.length, () => {
  scrollToBottom();
});

const formatTime = (iso: string) => {
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const getDisplayName = (conv: any) => {
    // If user is provider, show customer name. If user is customer, show provider name.
    // This depends on how the backend populates the conversation objects.
    // For now, let's use a placeholder.
    return authStore.user.id === conv.user_id ? `Provider #${conv.provider_id}` : `Customer #${conv.user_id}`;
};
</script>

<template>
  <div class="chat-page">
    <div class="chat-container">
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h2>Messages</h2>
        </div>
        <div class="conversation-list">
          <div 
            v-for="conv in messageStore.conversations" 
            :key="conv.id"
            class="conversation-item"
            :class="{ active: conv.id === messageStore.activeConversationId }"
            @click="selectConversation(conv.id)"
          >
            <div class="avatar">
              {{ getDisplayName(conv).charAt(0) }}
            </div>
            <div class="conv-info">
              <div class="conv-top">
                <span class="name">{{ getDisplayName(conv) }}</span>
                <span class="time">{{ formatTime(conv.updated_at) }}</span>
              </div>
              <p class="last-msg">{{ conv.last_message || 'No messages yet' }}</p>
            </div>
          </div>
          
          <div v-if="messageStore.conversations.length === 0" class="empty-state">
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
                <h3>{{ pendingShopName }} (New Chat)</h3>
              </template>
              <template v-else-if="messageStore.conversations.find(c => c.id === messageStore.activeConversationId)">
                <div class="avatar sm">
                  {{ getDisplayName(messageStore.conversations.find(c => c.id === messageStore.activeConversationId)).charAt(0) }}
                </div>
                <h3>{{ getDisplayName(messageStore.conversations.find(c => c.id === messageStore.activeConversationId)) }}</h3>
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
                @keyup.enter="sendMessage"
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
  </div>
</template>

<style scoped>
.chat-page {
  height: 100%;
  padding: 24px;
  background: var(--bg);
}

.chat-container {
  height: 100%;
  display: flex;
  background: #1c1c24;
  border: 1px solid var(--border);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.sidebar {
  width: 320px;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid var(--border);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  padding: 16px 24px;
  display: flex;
  gap: 12px;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.conversation-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.conversation-item.active {
  background: var(--accent-bg);
  border-right: 2px solid var(--accent);
}

.avatar {
  width: 48px;
  height: 48px;
  background: var(--accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  flex-shrink: 0;
}

.avatar.sm {
  width: 32px;
  height: 32px;
  font-size: 14px;
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
  color: var(--text-h);
}

.time {
  font-size: 12px;
  color: var(--text);
}

.last-msg {
  font-size: 13px;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #16161e;
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-info h3 {
  margin: 0;
  font-size: 16px;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-wrapper {
  display: flex;
  flex-direction: column;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  background: #2e2e3a;
  color: var(--text-h);
  position: relative;
}

.message-bubble p {
  margin: 0;
  font-size: 15px;
}

.msg-time {
  font-size: 10px;
  color: var(--text);
  margin-top: 4px;
  display: block;
  text-align: right;
}

.mine {
  align-items: flex-end;
}

.mine .message-bubble {
  background: var(--accent);
  color: white;
  border-bottom-right-radius: 4px;
}

.mine .msg-time {
  color: rgba(255, 255, 255, 0.7);
}

.chat-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--border);
}

.input-wrapper {
  display: flex;
  gap: 12px;
  background: #2e2e3a;
  padding: 8px 8px 8px 16px;
  border-radius: 16px;
  border: 1px solid transparent;
  transition: border-color 0.2s;
}

.input-wrapper:focus-within {
  border-color: var(--accent);
}

.input-wrapper input {
  flex: 1;
  background: none;
  border: none;
  color: var(--text-h);
  font-size: 15px;
}

.input-wrapper input:focus {
  outline: none;
}

.input-wrapper button {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--accent);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s;
}

.input-wrapper button:disabled {
  opacity: 0.5;
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text);
}

.empty-icon {
  margin-bottom: 20px;
  opacity: 0.2;
}

.chat-empty h3 {
  font-weight: 400;
  opacity: 0.5;
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text);
  opacity: 0.6;
}
</style>
