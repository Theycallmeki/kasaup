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
  customer_latitude?: number | null
  customer_longitude?: number | null
}) {
  const res = await api.post("/appointments", data)
  return res.data
}

export async function updateAppointment(id: number, data: {
  appointment_time?: string
}) {
  const res = await api.put(`/appointments/${id}`, data)
  return res.data
}

export async function deleteAppointment(id: number) {
  const res = await api.delete(`/appointments/${id}`)
  return res.data
}

export async function confirmAppointment(id: number) {
  const res = await api.put(`/appointments/${id}/confirm`)
  return res.data
}

export async function cancelAppointment(id: number) {
  const res = await api.put(`/appointments/${id}/cancel`)
  return res.data
}

export async function completeAppointment(id: number) {
  const res = await api.put(`/appointments/${id}/complete`)
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