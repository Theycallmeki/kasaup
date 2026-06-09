import { defineStore } from "pinia"
import {
  getOverview,
  getRecentActivity,
  getPendingUsers
} from "../services/admin"

export const useAdminStore = defineStore("admin", {
  state: () => ({
    overview: null as any,
    recentActivity: null as any,
    pendingUsers: [] as any[],
    loadingOverview: false,
    loadingActivity: false,
    loadingPending: false
  }),

  actions: {
    async fetchOverview() {
      this.loadingOverview = true
      try {
        this.overview = await getOverview()
      } finally {
        this.loadingOverview = false
      }
    },

    async fetchRecentActivity() {
      this.loadingActivity = true
      try {
        this.recentActivity = await getRecentActivity()
      } finally {
        this.loadingActivity = false
      }
    },

    async fetchPendingUsers() {
      this.loadingPending = true
      try {
        this.pendingUsers = await getPendingUsers()
      } finally {
        this.loadingPending = false
      }
    }
  }
})
