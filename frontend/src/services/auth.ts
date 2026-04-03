import api from "./api"

export const loginRequest = async (email: string, password: string) => {
  const res = await api.post("/auth/login/", { email, password })
  return res.data
}

export const logoutRequest = async () => {
  const res = await api.post("/auth/logout/")
  return res.data
}

export const getCurrentUser = async () => {
  const res = await api.get("/auth/me/")
  return res.data
}

export const registerRequest = async (data: {
  email: string
  password: string
  full_name?: string
  phone?: string
  role?: string
}) => {
  const res = await api.post("/users/", data)
  return res.data
}