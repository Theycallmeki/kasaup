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

        await loginRequest(email, password)

        this.user = await getCurrentUser()

      } finally {

        this.loading = false

      }

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