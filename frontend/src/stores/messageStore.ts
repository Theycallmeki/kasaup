import { defineStore } from "pinia"
import { getConversations, getConversationMessages, sendMessage, deleteConversation } from "../services/messages"
import api from "../services/api"

export const useMessageStore = defineStore("messages", {

  state: () => ({
    conversations: [] as any[],
    activeMessages: [] as any[],
    activeConversationId: null as number | null,
    loading: false,
    socket: null as WebSocket | null,
  }),

  getters: {
    totalUnreadCount: (state) => {
      return state.conversations.reduce((sum, c) => sum + (c.unread_count || 0), 0)
    }
  },

  actions: {

    async fetchConversations() {
      this.loading = true
      try {
        this.conversations = await getConversations()
      } finally {
        this.loading = false
      }
    },

    async fetchMessages(conversationId: number) {
      this.activeConversationId = conversationId
      this.activeMessages = await getConversationMessages(conversationId)
    },

    async send(receiverId: number, content: string | null, imageUrl: string | null = null) {
      const msg = await sendMessage(receiverId, content, imageUrl)

      if (this.activeConversationId === -1) {
        this.activeConversationId = msg.conversation_id
      }

      const index = this.conversations.findIndex(c => c.id === msg.conversation_id)
      if (index !== -1) {
        this.conversations[index].last_message = content || "Sent an image"
        this.conversations[index].updated_at = msg.created_at
      } else {
        await this.fetchConversations()
      }

      if (this.activeConversationId === msg.conversation_id) {
        const exists = this.activeMessages.some(m => m.id === msg.id)
        if (!exists) {
          this.activeMessages.push(msg)
        }
      }

      return msg
    },

    async deleteConversation(conversationId: number) {
      try {
        await deleteConversation(conversationId)
        this.conversations = this.conversations.filter(c => c.id !== conversationId)
        if (this.activeConversationId === conversationId) {
          this.activeConversationId = null
          this.activeMessages = []
        }
      } catch (err) {
        console.error("Failed to delete conversation", err)
        throw err
      }
    },

    async markAsRead(conversationId: number) {
      try {
        await api.put(`/messages/conversations/${conversationId}/read/`)
        const index = this.conversations.findIndex(c => c.id === conversationId)
        if (index !== -1) {
          this.conversations[index].unread_count = 0
        }
      } catch (err) {
        console.error("Failed to mark as read", err)
      }
    },

    connectWS(userId: number) {
      if (this.socket) return

      const baseUrl = import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.host}`
      
      let wsUrl: string;
      if (baseUrl.startsWith("http")) {
        wsUrl = `${baseUrl.replace("http", "ws")}/messages/ws`;
      } else {
        // Handle relative paths (like /api)
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const host = window.location.host;
        wsUrl = `${protocol}//${host}${baseUrl}/messages/ws`;
      }

      this.socket = new WebSocket(wsUrl);

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === "new_message") {
          this.handleIncomingMessage(data.data)
        }
      }

      this.socket.onclose = () => {
        this.socket = null
        setTimeout(() => this.connectWS(userId), 5000)
      }
    },

    handleIncomingMessage(message: any) {
      if (this.activeConversationId === message.conversation_id) {
        const exists = this.activeMessages.some(m => m.id === message.id)
        if (!exists) {
          this.activeMessages.push(message)
        }
      }

      const index = this.conversations.findIndex(c => c.id === message.conversation_id)
      if (index !== -1) {
        this.conversations[index].last_message = message.content || "Sent an image"
        this.conversations[index].updated_at = message.created_at
        const conv = this.conversations.splice(index, 1)[0]

        if (this.activeConversationId !== message.conversation_id) {
          conv.unread_count = (conv.unread_count || 0) + 1
        } else {
          this.markAsRead(message.conversation_id)
        }

        this.conversations.unshift(conv)
      } else {
        this.fetchConversations()
      }
    }

  }

})
