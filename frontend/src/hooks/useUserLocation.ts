import { useAuthStore } from "../stores/authStore"

export function useUserLocation() {
  const auth = useAuthStore()

  const getSavedLocation = () => {
    if (!auth.user) return null
    
    return {
      address: auth.user.address || "",
      latitude: auth.user.latitude || null,
      longitude: auth.user.longitude || null
    }
  }

  const hasSavedLocation = () => {
    return !!(auth.user?.latitude && auth.user?.longitude)
  }

  return {
    getSavedLocation,
    hasSavedLocation,
    user: auth.user
  }
}
