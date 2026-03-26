import { defineStore } from "pinia";
import {
  getServices,
  getProviderServices,
  createService,
  updateService,
  deleteService,
  uploadServiceImages,
  deleteServiceImage
} from "../services/services";

export const useServiceStore = defineStore("services", {
  state: () => ({
    services: [] as any[],
    loading: false,
  }),

  actions: {
    async fetchServices() {
      this.loading = true;

      try {
        this.services = await getServices();
      } finally {
        this.loading = false;
      }
    },

    async fetchProviderServices(providerId: number) {
      this.loading = true;

      try {
        this.services = await getProviderServices(providerId);
      } finally {
        this.loading = false;
      }
    },

    async addService(data: any) {
      const service = await createService(data);
      await this.fetchServices();
      return service;
    },

    async editService(id: number, data: any) {
      const service = await updateService(id, data);
      await this.fetchServices();
      return service;
    },

    async removeService(id: number) {
      const res = await deleteService(id);
      await this.fetchServices();
      return res;
    },

    async uploadImages(serviceId: number, files: File[]) {
      const res = await uploadServiceImages(serviceId, files);
      await this.fetchServices();
      return res;
    },

    async removeServiceImage(serviceId: number, imageId: number) {
      const res = await deleteServiceImage(serviceId, imageId);
      await this.fetchServices();
      return res;
    },
  },
});