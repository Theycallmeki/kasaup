import api from "./api"

export async function getAppointments() {
  const res = await api.get("/appointments")
  return res.data
}

export async function createAppointment(data: {
  provider_id: number
  service_id: number
  appointment_time: string
  status?: string
}) {
  const res = await api.post("/appointments", data)
  return res.data
}

export async function getAvailableSlots(serviceId: number) {
  const res = await api.get(`/appointments/services/${serviceId}/available-slots`)
  return res.data.available_slots
}