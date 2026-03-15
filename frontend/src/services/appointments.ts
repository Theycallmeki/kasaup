import api from "./api"

export async function getAppointments() {
  const res = await api.get("/appointments")
  return res.data
}

export async function getAppointment(id: number) {
  const res = await api.get(`/appointments/${id}`)
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

export async function updateAppointment(id: number, data: any) {
  const res = await api.put(`/appointments/${id}`, data)
  return res.data
}

export async function deleteAppointment(id: number) {
  const res = await api.delete(`/appointments/${id}`)
  return res.data
}

export async function getAvailableSlots(serviceId: number) {
  const res = await api.get(`/appointments/services/${serviceId}/available-slots`)
  return res.data.available_slots
}

export async function getProviderSlots(providerId: number) {
  const res = await api.get(`/appointments/providers/${providerId}/available-slots`)
  return res.data.available_slots
}