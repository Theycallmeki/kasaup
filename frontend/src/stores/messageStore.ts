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

    async send(receiverId: number, content: string) {
      const msg = await sendMessage(receiverId, content)
      
      // If this was a new conversation (pending ID -1), sync the ID now
      if (this.activeConversationId === -1) {
          this.activeConversationId = msg.conversation_id
      }

      // Check if we already have this conversation in the list
      const index = this.conversations.findIndex(c => c.id === msg.conversation_id)
      if (index !== -1) {
        this.conversations[index].last_message = content
        this.conversations[index].updated_at = msg.created_at
      } else {
        await this.fetchConversations()
      }
      
      // Push the message if it belongs to the active conversation
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
      const wsUrl = `${baseUrl.replace("http", "ws")}/messages/ws`
      this.socket = new WebSocket(wsUrl)

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === "new_message") {
          this.handleIncomingMessage(data.data)
        }
      }

      this.socket.onclose = () => {
        this.socket = null
        // Optional: auto-reconnect
        setTimeout(() => this.connectWS(userId), 5000)
      }
    },

    handleIncomingMessage(message: any) {
      // If we are looking at this conversation, push it (if not already there)
      if (this.activeConversationId === message.conversation_id) {
        const exists = this.activeMessages.some(m => m.id === message.id)
        if (!exists) {
            this.activeMessages.push(message)
        }
      }

      // Update the conversation list preview
      const index = this.conversations.findIndex(c => c.id === message.conversation_id)
      if (index !== -1) {
        this.conversations[index].last_message = message.content
        this.conversations[index].updated_at = message.created_at
        // Move to top
        const conv = this.conversations.splice(index, 1)[0]
        
        // Only increment unread if not the active conversation
        if (this.activeConversationId !== message.conversation_id) {
           conv.unread_count = (conv.unread_count || 0) + 1
        } else {
           // If it is the active one, mark as read on server immediately
           this.markAsRead(message.conversation_id)
        }
        
        this.conversations.unshift(conv)
      } else {
        this.fetchConversations()
      }
    }

  }

})
