import { defineStore } from "pinia"
import {
  getAppointments,
  createAppointment,
  getAvailableSlots,
  confirmAppointment,
  cancelAppointment,
  completeAppointment
} from "../services/appointments"

export const useAppointmentStore = defineStore("appointments", {

  state: () => ({
    appointments: [] as any[],
    slots: [] as string[],
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

    async bookAppointment(data: {
      provider_id: number
      service_id: number
      appointment_time: string
      customer_latitude?: number | null
      customer_longitude?: number | null
    }) {
      const res = await createAppointment(data)
      await this.fetchAppointments()
      return res
    },

    async confirm(id: number) {
      await confirmAppointment(id)
      await this.fetchAppointments()
    },

    async cancel(id: number) {
      await cancelAppointment(id)
      await this.fetchAppointments()
    },

    async complete(id: number) {
      await completeAppointment(id)
      await this.fetchAppointments()
    }

  }

})