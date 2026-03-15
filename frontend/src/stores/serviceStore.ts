import { defineStore } from "pinia"
import { getServices } from "../services/services"

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

    }

  }

})