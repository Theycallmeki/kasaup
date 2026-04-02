import axios from "axios"

const baseURL = import.meta.env.VITE_API_URL || "/api"

const api = axios.create({
  baseURL,
  withCredentials: true
})

api.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    if (error.response?.status === 401) {
      // Handle unauthorized if needed
    }
    return Promise.reject(error)
  }
)

export default api