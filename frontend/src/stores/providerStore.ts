import { defineStore } from "pinia"
import {
  getProviders,
  getProvider,
  getProviderProfile,
  createProvider,
  updateProvider,
  deleteProvider,
  uploadProviderImage,
  getMyProvider,
  updateMyProvider
} from "../services/providers"

export const useProviderStore = defineStore("providers", {

  state: () => ({
    providers: [] as any[],
    provider: null as any,
    providerProfile: null as any,
    myProvider: null as any,
    loading: false
  }),

  actions: {

    async fetchProviders() {
      this.loading = true
      try {
        this.providers = await getProviders({ limit: 500, offset: 0 })
      } finally {
        this.loading = false
      }
    },

    async fetchProvider(id: number) {
      this.loading = true
      try {
        this.provider = await getProvider(id)
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
    },

    async fetchMyProvider() {
      this.loading = true
      try {
        this.myProvider = await getMyProvider()
      } catch {
        this.myProvider = null
      } finally {
        this.loading = false
      }
    },

    async addProvider(data: any) {
      const res = await createProvider(data)
      await this.fetchProviders()
      await this.fetchMyProvider()
      return res
    },

    async editProvider(id: number, data: any) {
      const res = await updateProvider(id, data)
      await this.fetchProviders()
      return res
    },

    async updateMy(data: any) {
      const res = await updateMyProvider(data)
      await this.fetchMyProvider()
      return res
    },

    async removeProvider(id: number) {
      const res = await deleteProvider(id)
      await this.fetchProviders()
      return res
    },

    async uploadProfileImage(providerId: number, file: File) {
      const res = await uploadProviderImage(providerId, file)
      await this.fetchProvider(providerId)
      await this.fetchMyProvider()
      return res
    }

  }

})