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

  actions: {
    async login(email: string, password: string) {
      this.loading = true
      this.user = await loginRequest(email, password)
      this.loading = false
    },

    async logout() {
      await logoutRequest()
      this.user = null
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
