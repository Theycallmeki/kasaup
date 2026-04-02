import api from "./api"

export async function getServices() {
  const res = await api.get("/services/")
  return res.data
}

export async function getService(id: number) {
  const res = await api.get(`/services/${id}`)
  return res.data
}

export async function getProviderServices(providerId: number) {
  const res = await api.get(`/services/provider/${providerId}`)
  return res.data
}

export async function getCategoryServices(categoryId: number) {
  const res = await api.get(`/services/category/${categoryId}`)
  return res.data
}

export async function searchServices(params: {
  q?: string
  category_id?: number
  min_price?: number
  max_price?: number
}) {
  const res = await api.get("/services/search", { params })
  return res.data
}

export async function createService(data: {
  category_id: number
  name: string
  description?: string
  price: number
  duration_minutes: number
}) {
  const res = await api.post("/services/", data)
  return res.data
}

export async function updateService(id: number, data: {
  category_id?: number
  name?: string
  description?: string
  price?: number
  duration_minutes?: number
}) {
  const res = await api.put(`/services/${id}`, data)
  return res.data
}

export async function deleteService(id: number) {
  const res = await api.delete(`/services/${id}`)
  return res.data
}

export async function uploadServiceImages(serviceId: number, files: File[]) {
  const formData = new FormData()

  files.forEach(file => {
    formData.append("files", file)
  })

  const res = await api.post(
    `/services/${serviceId}/images`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  )

  return res.data
}

export async function deleteServiceImage(serviceId: number, imageId: number) {
  const res = await api.delete(`/services/${serviceId}/images/${imageId}`)
  return res.data
}