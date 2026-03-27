import { defineStore } from "pinia"
import {
  getAppointments,
  createAppointment,
  getAvailableSlots,
  approveAppointment,
  cancelAppointment,
  completeAppointment
} from "../services/appointments"

function toISO(date: string, time: string) {
  return `${date}T${time}`
}

export const useAppointmentStore = defineStore("appointments", {

  state: () => ({
    appointments: [] as any[],
    slots: [] as string[],
    loading: false,
    selectedDate: "" as string
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

    async fetchAvailableSlots(serviceId: number, date: string) {
      this.loading = true
      try {
        this.selectedDate = date
        this.slots = await getAvailableSlots(serviceId, date)
      } finally {
        this.loading = false
      }
    },

    async bookAppointment(data: {
      provider_id: number
      service_id: number
      date: string
      time: string
      customer_latitude?: number | null
      customer_longitude?: number | null
    }) {
      const res = await createAppointment({
        provider_id: data.provider_id,
        service_id: data.service_id,
        appointment_time: toISO(data.date, data.time),
        customer_latitude: data.customer_latitude,
        customer_longitude: data.customer_longitude
      })

      await this.fetchAppointments()
      return res
    },

    async approve(id: number) {
      await approveAppointment(id)
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