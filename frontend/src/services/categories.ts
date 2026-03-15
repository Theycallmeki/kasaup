import api from "./api"

export async function getCategories() {
  const res = await api.get("/categories")
  return res.data
}

export async function getCategory(id: number) {
  const res = await api.get(`/categories/${id}`)
  return res.data
}

export async function getCategoryServices(id: number) {
  const res = await api.get(`/categories/${id}/services`)
  return res.data
}

export async function createCategory(data: { name: string }) {
  const res = await api.post("/categories", data)
  return res.data
}

export async function updateCategory(id: number, data: { name: string }) {
  const res = await api.put(`/categories/${id}`, data)
  return res.data
}

export async function deleteCategory(id: number) {
  const res = await api.delete(`/categories/${id}`)
  return res.data
}