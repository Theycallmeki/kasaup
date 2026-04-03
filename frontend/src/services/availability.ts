import api from "./api"

function formatTo12h(time: string) {
  const [hour, minute] = time.split(":").map(Number)

  const date = new Date()
  date.setHours(hour, minute)

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  })
}

export async function getAvailability(providerId: number) {
  const res = await api.get(`/availability/${providerId}/`)
  return res.data
}

export async function createAvailability(data: {
  provider_id: number
  day_of_week: number
  start_time: string
  end_time: string
}) {
  const res = await api.post("/availability/", {
    ...data,
    start_time: formatTo12h(data.start_time),
    end_time: formatTo12h(data.end_time)
  })
  return res.data
}

export async function updateAvailability(id: number, data: {
  day_of_week?: number
  start_time?: string
  end_time?: string
}) {
  const res = await api.put(`/availability/${id}/`, {
    ...data,
    start_time: data.start_time ? formatTo12h(data.start_time) : undefined,
    end_time: data.end_time ? formatTo12h(data.end_time) : undefined
  })
  return res.data
}

export async function deleteAvailability(id: number) {
  const res = await api.delete(`/availability/${id}/`)
  return res.data
}