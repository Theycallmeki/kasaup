import axios from "axios"

const baseURL = import.meta.env.VITE_API_URL || "https://167.172.66.181.nip.io"

const api = axios.create({
  baseURL,
  withCredentials: true
})

// Removed localStorage-based Authorization header interceptor.
// Cookies are automatically sent with `withCredentials: true`.

api.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    if (error.response?.status === 401) {
    }
    return Promise.reject(error)
  }
)

export default api