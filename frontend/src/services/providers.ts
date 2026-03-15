import api from "./api"

export async function getProviders() {
  const res = await api.get("/providers")
  return res.data
}

export async function getProvider(id: number) {
  const res = await api.get(`/providers/${id}`)
  return res.data
}

export async function getProviderProfile(id: number) {
  const res = await api.get(`/providers/${id}/profile`)
  return res.data
}

export async function getNearbyProviders(
  lat: number,
  lng: number,
  radius: number = 10
) {
  const res = await api.get("/providers/nearby", {
    params: { lat, lng, radius }
  })
  return res.data
}