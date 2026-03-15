import { defineStore } from "pinia"
import {
  getServices,
  getProviderServices,
  createService,
  updateService,
  deleteService
} from "../services/services"

export const useServiceStore = defineStore("services", {

  state: () => ({
    services: [] as any[],
    loading: false
  }),

  actions: {

    async fetchServices() {

      this.loading = true

      try {
        this.services = await getServices()
      } finally {
        this.loading = false
      }

    },

    async fetchProviderServices(providerId: number) {

      this.loading = true

      try {
        this.services = await getProviderServices(providerId)
      } finally {
        this.loading = false
      }

    },

    async addService(data: any) {
      return await createService(data)
    },

    async editService(id: number, data: any) {
      return await updateService(id, data)
    },

    async removeService(id: number) {
      return await deleteService(id)
    }

  }

})