import api from "./api"

export async function getAvailability(providerId: number) {
  const res = await api.get(`/availability/${providerId}`)
  return res.data
}

export async function createAvailability(data: {
  provider_id: number
  day_of_week: number
  start_time: string
  end_time: string
}) {
  const res = await api.post("/availability", data)
  return res.data
}

export async function updateAvailability(id: number, data: {
  day_of_week?: number
  start_time?: string
  end_time?: string
}) {
  const res = await api.put(`/availability/${id}`, data)
  return res.data
}

export async function deleteAvailability(id: number) {
  const res = await api.delete(`/availability/${id}`)
  return res.data
}