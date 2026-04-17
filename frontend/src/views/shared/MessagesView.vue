<script setup lang="ts">
import { onMounted, ref, watch, reactive } from 'vue';
import { uploadMessageImage } from '../../services/messages';
import { useScroll } from '../../hooks/useScroll';
import { useRoute } from 'vue-router';
import { useMessageStore } from '../../stores/messageStore';
import { useAuthStore } from '../../stores/authStore';
import { computed } from 'vue';
import api from '../../services/api';

const route = useRoute();
const messageStore = useMessageStore();
const authStore = useAuthStore();

const newMessage = ref('');
const { scrollRef: messagesDropdown, scrollToBottom } = useScroll();

const pendingReceiverId = ref<number | null>(null);
const pendingShopName = ref<string | null>(null);

const showDeleteConfirm = ref(false);
const conversationToDelete = ref<any>(null);

// Mobile panel state: 'list' | 'chat'
const mobilePanel = ref<'list' | 'chat'>('list');

// Desktop sidebar collapsed state
const sidebarCollapsed = ref(false);
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value;
};

const uploadingImage = ref(false);
const imageInput = ref<HTMLInputElement | null>(null);

// Full-screen image viewer state
const viewerOpen = ref(false);
const viewerSrc = ref('');
const viewerClosing = ref(false);

// Track loaded state per message id
const imageLoaded = reactive<Record<number, boolean>>({});
// Track error state per message id
const imageError = reactive<Record<number, boolean>>({});

const selectedImageFile = ref<File | null>(null);
const imagePreviewUrl = ref<string | null>(null);

const openViewer = (src: string) => {
  viewerSrc.value = src;
  viewerClosing.value = false;
  viewerOpen.value = true;
};

const closeViewer = () => {
  viewerClosing.value = true;
  setTimeout(() => {
    viewerOpen.value = false;
    viewerClosing.value = false;
    viewerSrc.value = '';
  }, 220);
};

const downloadImage = async () => {
  try {
    const response = await fetch(viewerSrc.value);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'image_' + Date.now() + '.jpg';
    a.click();
    URL.revokeObjectURL(url);
  } catch {
    window.open(viewerSrc.value, '_blank');
  }
};

const triggerImageUpload = () => {
  imageInput.value?.click();
};

const handleImageSelected = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  // Validate file type
  if (!file.type.startsWith('image/')) {
    alert('Please select an image file.');
    return;
  }

  // Validate file size (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    alert('Image must be smaller than 10MB.');
    return;
  }

  selectedImageFile.value = file;
  if (imagePreviewUrl.value) URL.revokeObjectURL(imagePreviewUrl.value);
  imagePreviewUrl.value = URL.createObjectURL(file);
  if (imageInput.value) imageInput.value.value = '';
};

const clearSelectedImage = () => {
  selectedImageFile.value = null;
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value);
    imagePreviewUrl.value = null;
  }
};

const sendMessageInternal = async (content: string | null, imageUrl: string | null = null) => {
  let targetReceiverId: number | null = null;

  if (messageStore.activeConversationId === -1 && pendingReceiverId.value) {
    targetReceiverId = pendingReceiverId.value;
  } else if (messageStore.activeConversationId) {
    const conv = messageStore.conversations.find(c => c.id === messageStore.activeConversationId);
    if (conv) {
      targetReceiverId = authStore.user!.id === conv.user_id
        ? conv.provider_owner_id
        : conv.user_id;
    }
  }

  if (!targetReceiverId) {
    console.error('Could not determine recipient ID');
    return;
  }

  try {
    const msg = await messageStore.send(targetReceiverId, content, imageUrl);
    if (content) newMessage.value = '';

    if (messageStore.activeConversationId === -1) {
      messageStore.activeConversationId = msg.conversation_id;
      pendingReceiverId.value = null;
      pendingShopName.value = null;
      await messageStore.fetchConversations();
    }

    scrollToBottom();
  } catch (err) {
    console.error('Failed to send message', err);
  }
};

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
  if (!newMessage.value.trim() && !selectedImageFile.value) return;
  
  let imageUrl: string | null = null;
  
  if (selectedImageFile.value) {
    uploadingImage.value = true;
    try {
      imageUrl = await uploadMessageImage(selectedImageFile.value);
      clearSelectedImage();
    } catch (err) {
      alert('Failed to upload image. Please try again.');
      uploadingImage.value = false;
      return;
    } finally {
      uploadingImage.value = false;
    }
  }

  await sendMessageInternal(newMessage.value.trim() || null, imageUrl);
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
    alert('Failed to delete conversation');
  }
};

watch(() => messageStore.activeMessages.length, () => {
  scrollToBottom();
});

// Close viewer on Escape key
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && viewerOpen.value) closeViewer();
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

import { onUnmounted } from 'vue';
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

const formatTime = (iso: string) => {
  if (!iso) return '';
  const dateStr = iso.includes('T') ? iso : iso.replace(' ', 'T');
  return new Date(dateStr).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
};

const getDisplayName = (conv: any) => {
  if (!authStore.user) return '';
  if (authStore.user.id === conv.user_id) return conv.shop_name;
  return conv.user_name;
};

const imgUrl = (path: string) => {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  return `${api.defaults.baseURL}${path.startsWith('/') ? path : '/' + path}`;
};

const activeConversation = computed(() => {
  if (!messageStore.activeConversationId) return null;
  if (messageStore.activeConversationId === -1) return null;
  return messageStore.conversations.find(c => c.id === messageStore.activeConversationId) || null;
});
</script>

<template>
  <div class="page full-height" :data-panel="mobilePanel">
    <div class="page-header">
      <h1 class="title">Messages</h1>
      <p class="hint">Keep in touch with your service providers and clients.</p>
    </div>

    <div class="chat-container" :class="{ 'sidebar-hidden': sidebarCollapsed }">
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
              <p class="last-msg">
                <!-- Show image icon hint in sidebar if last message is an image -->
                <span v-if="conv.last_message_type === 'image'" class="last-msg-img-hint">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline;vertical-align:middle;margin-right:3px"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
                  Photo
                </span>
                <span v-else>{{ conv.last_message || 'No messages yet' }}</span>
              </p>
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
            <button class="back-btn" @click="goBackToList" aria-label="Back to conversations">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 5l-7 7 7 7" />
              </svg>
            </button>
            <button class="sidebar-toggle-btn" @click="toggleSidebar" :aria-label="sidebarCollapsed ? 'Show conversations' : 'Hide conversations'" :title="sidebarCollapsed ? 'Show conversations' : 'Hide conversations'">
              <svg v-if="!sidebarCollapsed" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M9 3v18" />
              </svg>
              <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M9 3v18" />
                <path d="M14 9l3 3-3 3" />
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
              :class="{
                'mine': msg.sender_id === authStore.user?.id,
                'is-image-only': msg.image_url && !msg.content,
              }"
            >
              <div
                class="message-bubble"
                :class="{ 'image-only': msg.image_url && !msg.content }"
              >
                <!-- Image attachment -->
                <div
                  v-if="msg.image_url"
                  class="msg-image-wrap"
                  :class="{ 'has-text': !!msg.content }"
                >
                  <!-- Skeleton shown until loaded or on error -->
                  <div
                    v-if="!imageLoaded[msg.id] && !imageError[msg.id]"
                    class="img-skeleton"
                  >
                    <div class="img-shimmer" />
                  </div>

                  <!-- Error fallback -->
                  <div v-if="imageError[msg.id]" class="img-error">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M3 3l18 18M10.5 10.67A2 2 0 0 0 8 12.5v.5H6l-3 3V5a2 2 0 0 1 2-2h10.5M21 15l-3-3-1.5 1.5M21 5a2 2 0 0 0-2-2h-7"/>
                    </svg>
                    <span>Failed to load</span>
                  </div>

                  <!-- Actual image -->
                  <div
                    v-show="imageLoaded[msg.id] && !imageError[msg.id]"
                    class="img-clickable"
                    @click="openViewer(imgUrl(msg.image_url))"
                    role="button"
                    tabindex="0"
                    @keydown.enter="openViewer(imgUrl(msg.image_url))"
                    aria-label="View full size image"
                  >
                    <img
                      :src="imgUrl(msg.image_url)"
                      alt="Attachment"
                      class="msg-img"
                      @load="imageLoaded[msg.id] = true"
                      @error="imageError[msg.id] = true"
                    />
                    <!-- Hover overlay -->
                    <div class="img-hover-overlay" aria-hidden="true">
                      <div class="img-expand-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2">
                          <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" />
                        </svg>
                      </div>
                    </div>
                    <!-- Timestamp overlaid on image when no text -->
                    <span v-if="!msg.content" class="img-time-overlay">{{ formatTime(msg.created_at) }}</span>
                  </div>
                </div>

                <!-- Text content -->
                <p v-if="msg.content" class="text-content">{{ msg.content }}</p>

                <!-- Timestamp shown below text (or below image if has text) -->
                <span v-if="msg.content || !msg.image_url" class="msg-time">{{ formatTime(msg.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="chat-footer">
            <!-- Image Preview Bar -->
            <div v-if="imagePreviewUrl" class="image-preview-bar">
              <div class="preview-item">
                <img :src="imagePreviewUrl" alt="Preview" />
                <button class="remove-preview" @click="clearSelectedImage" title="Remove image">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 6 6 18M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="input-wrapper">
              <input
                type="file"
                accept="image/*"
                ref="imageInput"
                @change="handleImageSelected"
                style="display: none;"
              />
              <button class="attach-btn" @click="triggerImageUpload" :disabled="uploadingImage" title="Attach Image">
                <svg v-if="!uploadingImage" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                </svg>
              </button>
              <input
                v-model="newMessage"
                @keydown.enter.prevent="sendMessage"
                placeholder="Type a message..."
              />
              <button @click="sendMessage" :disabled="!newMessage.trim() && !selectedImageFile" :class="{ loading: uploadingImage }">
                <svg v-if="!uploadingImage" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" />
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

    <!-- Full-screen Image Viewer -->
    <Teleport to="body">
      <div
        v-if="viewerOpen"
        class="img-viewer-overlay"
        :class="{ closing: viewerClosing }"
        @click.self="closeViewer"
      >
        <div class="img-viewer-inner" :class="{ closing: viewerClosing }">
          <button class="viewer-close-btn" @click="closeViewer" aria-label="Close image viewer">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
          <img :src="viewerSrc" alt="Full size image" class="viewer-img" />
          <div class="viewer-actions">
            <button class="viewer-action-btn" @click="downloadImage">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" />
              </svg>
              Save image
            </button>
            <button class="viewer-action-btn" @click="closeViewer">Close</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
@import "../../styles/shared/MessagesView.css";
</style>