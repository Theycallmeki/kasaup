import { defineStore } from "pinia"
import {
  loginRequest,
  logoutRequest,
  getCurrentUser,
  registerRequest
} from "../services/auth"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as any,
    loading: false
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    role: (state) => state.user?.role || null
  },

  actions: {

    async login(email: string, password: string) {
      this.loading = true
      try {
        const response = await loginRequest(email, password)
        // Manual login also sets cookies on the backend, 
        // but it doesn't return tokens in JSON unless we changed the backend.
        // If the backend doesn't return them, Axios withCredentials will handle it.
        // However, for the "Handshake" we should also have them if possible.
        this.user = await getCurrentUser()
      } finally {
        this.loading = false
      }
    },

    async logout() {
      await logoutRequest()
      this.user = null
      // Clear localStorage tokens
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
    },

    async fetchUser() {

      try {

        this.user = await getCurrentUser()

      } catch {

        this.user = null

      }

    },

    async register(data: any) {

      return await registerRequest(data)

    }

  }
})