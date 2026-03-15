import { defineStore } from "pinia"
import {
  getProviders,
  getProviderProfile
} from "../services/providers"

export const useProviderStore = defineStore("providers", {

  state: () => ({
    providers: [] as any[],
    providerProfile: null as any,
    loading: false
  }),

  actions: {

    async fetchProviders() {

      this.loading = true

      try {
        this.providers = await getProviders()
      } finally {
        this.loading = false
      }

    },

    async fetchProviderProfile(id: number) {

      this.loading = true

      try {
        this.providerProfile = await getProviderProfile(id)
      } finally {
        this.loading = false
      }

    }

  }

})