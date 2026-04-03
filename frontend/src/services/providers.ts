import api from "./api"

export async function getProviders(params?: { limit?: number; offset?: number }) {
  const res = await api.get("/providers/", { params })
  return res.data
}

export async function getProvider(id: number) {
  const res = await api.get(`/providers/${id}/`)
  return res.data
}

export async function getProviderProfile(id: number) {
  const res = await api.get(`/providers/${id}/profile/`)
  return res.data
}

export async function getNearbyProviders(
  lat: number,
  lng: number,
  radius: number = 10
) {
  const res = await api.get("/providers/nearby/", {
    params: { lat, lng, radius }
  })
  return res.data
}

export async function getProvidersInMap(bounds: {
  min_lat: number
  max_lat: number
  min_lng: number
  max_lng: number
}) {
  const res = await api.get("/providers/map/", {
    params: {
      min_lat: bounds.min_lat,
      max_lat: bounds.max_lat,
      min_lng: bounds.min_lng,
      max_lng: bounds.max_lng
    }
  })
  return res.data
}

export async function createProvider(data: {
  shop_name: string
  description?: string
  phone?: string
  email?: string
  address?: string
  latitude: number
  longitude: number
  offers_home_service: boolean
}) {
  const res = await api.post("/providers/", data)
  return res.data
}

export async function updateProvider(id: number, data: {
  shop_name?: string
  description?: string
  phone?: string
  email?: string
  address?: string
  latitude?: number
  longitude?: number
  offers_home_service?: boolean
}) {
  const res = await api.put(`/providers/${id}/`, data)
  return res.data
}

export async function deleteProvider(id: number) {
  const res = await api.delete(`/providers/${id}/`)
  return res.data
}

export async function uploadProviderImage(providerId: number, file: File) {
  const formData = new FormData()
  formData.append("file", file)

  const res = await api.post(
    `/providers/${providerId}/profile-image/`,
    formData
  )

  return res.data
}

export async function getMyProvider() {
  const res = await api.get("/providers/me/")
  return res.data
}

export async function updateMyProvider(data: any) {
  const res = await api.put("/providers/me/", data)
  return res.data
}