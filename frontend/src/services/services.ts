import api from "./api"

export async function getServices() {
  const res = await api.get("/services")
  return res.data
}

export async function getService(id: number) {
  const res = await api.get(`/services/${id}`)
  return res.data
}

export async function searchServices(query: string) {
  const res = await api.get("/services/search", {
    params: { q: query }
  })
  return res.data
}