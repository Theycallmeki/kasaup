import api from "./api"

export async function getCategories() {
  const res = await api.get("/categories")
  return res.data
}