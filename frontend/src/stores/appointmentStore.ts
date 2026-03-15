import { defineStore } from "pinia"
import {
  getAppointments,
  createAppointment,
  getAvailableSlots
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
    }) {
      return await createAppointment(data)
    }

  }

})