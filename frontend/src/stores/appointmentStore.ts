import { defineStore } from "pinia"
import {
  getAppointments,
  createAppointment,
  getAvailableSlots
} from "../services/appointments"

export const useAppointmentStore = defineStore("appointments", {

  state: () => ({
    appointments: [] as any[],
    slots: [] as any[],
    loading: false
  }),

  actions: {

    async fetchAppointments() {

      this.loading = true

      try {
        this.appointments = await getAppointments()
      } finally {
        this.loading = false
      }

    },

    async fetchAvailableSlots(serviceId: number) {

      this.loading = true

      try {
        this.slots = await getAvailableSlots(serviceId)
      } finally {
        this.loading = false
      }

    },

    async bookAppointment(data: any) {
      return await createAppointment(data)
    }

  }

})