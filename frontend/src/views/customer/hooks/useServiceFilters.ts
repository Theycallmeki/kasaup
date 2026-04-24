import { computed, ref, type Ref } from "vue"
import { searchServices } from "../../../services/services"

type SortOption = "price_asc" | "price_desc" | "duration"

export function useServiceFilters(params: {
  svcStore: any
  providerMap: Ref<Record<number, any>>
  startLoading: (message?: string) => void
  stopLoading: () => void
}) {
  const { svcStore, providerMap, startLoading, stopLoading } = params

  const query = ref("")
  const activeCat = ref<number | "all">("all")
  const sort = ref<SortOption>("price_asc")
  const minPrice = ref<number | null>(null)
  const maxPrice = ref<number | null>(null)
  const minRating = ref<number>(0)
  const maxDistance = ref<number | null>(null)
  const useLocation = ref(false)

  const tempActiveCat = ref<number | "all">("all")
  const tempSort = ref<SortOption>("price_asc")
  const tempMinPrice = ref<number | null>(null)
  const tempMaxPrice = ref<number | null>(null)
  const tempMinRating = ref<number>(0)
  const tempMaxDistance = ref<number | null>(null)
  const tempUseLocation = ref(false)

  const showFilters = ref(false)
  const locLoading = ref(false)
  const currentLat = ref<number | null>(null)
  const currentLng = ref<number | null>(null)
  const searching = ref(false)

  const haversine = (lat1: number, lon1: number, lat2: number, lon2: number) => {
    const R = 6371
    const dLat = ((lat2 - lat1) * Math.PI) / 180
    const dLon = ((lon2 - lon1) * Math.PI) / 180
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
  }

  async function fetchCurrentLocation() {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser")
      return
    }
    startLoading("Detecting your location...")
    locLoading.value = true
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentLat.value = pos.coords.latitude
        currentLng.value = pos.coords.longitude
        tempUseLocation.value = true
        locLoading.value = false
        stopLoading()
      },
      (err) => {
        console.error("Location error:", err)
        alert("Could not get your location. Please check your browser permissions.")
        tempUseLocation.value = false
        locLoading.value = false
        stopLoading()
      },
      { timeout: 10000 }
    )
  }

  function toggleLocation() {
    if (!tempUseLocation.value) {
      fetchCurrentLocation()
    } else {
      tempUseLocation.value = false
    }
  }

  function openFilters() {
    tempActiveCat.value = activeCat.value
    tempSort.value = sort.value
    tempMinPrice.value = minPrice.value
    tempMaxPrice.value = maxPrice.value
    tempMinRating.value = minRating.value
    tempMaxDistance.value = maxDistance.value
    tempUseLocation.value = useLocation.value
    showFilters.value = true
  }

  function cancelFilters() {
    showFilters.value = false
  }

  function applyFilters() {
    activeCat.value = tempActiveCat.value
    sort.value = tempSort.value
    minPrice.value = tempMinPrice.value
    maxPrice.value = tempMaxPrice.value
    minRating.value = tempMinRating.value
    maxDistance.value = tempMaxDistance.value
    useLocation.value = tempUseLocation.value
    showFilters.value = false
  }

  function clearFilters() {
    tempActiveCat.value = "all"
    tempSort.value = "price_asc"
    tempMinPrice.value = null
    tempMaxPrice.value = null
    tempMinRating.value = 0
    tempMaxDistance.value = null
    tempUseLocation.value = false
  }

  const filtered = computed(() => {
    let list = svcStore.services

    if (activeCat.value !== "all") {
      list = list.filter((s: any) => s.category_id === activeCat.value)
    }

    if (query.value.trim()) {
      const q = query.value.toLowerCase()
      list = list.filter(
        (s: any) =>
          s.name?.toLowerCase().includes(q) ||
          s.description?.toLowerCase().includes(q) ||
          providerMap.value[s.provider_id]?.shop_name?.toLowerCase().includes(q)
      )
    }

    if (minPrice.value !== null) {
      list = list.filter((s: any) => s.price >= (minPrice.value || 0))
    }
    if (maxPrice.value !== null) {
      list = list.filter((s: any) => s.price <= (maxPrice.value || Infinity))
    }

    if (minRating.value > 0) {
      list = list.filter((s: any) => {
        const p = providerMap.value[s.provider_id]
        return (p?.rating || 0) >= minRating.value
      })
    }

    if (useLocation.value && maxDistance.value !== null && currentLat.value && currentLng.value) {
      list = list.filter((s: any) => {
        const p = providerMap.value[s.provider_id]
        if (!p?.latitude || !p?.longitude) return false
        const dist = haversine(currentLat.value!, currentLng.value!, p.latitude, p.longitude)
        return dist <= (maxDistance.value || Infinity)
      })
    }

    return [...list].sort((a: any, b: any) => {
      if (sort.value === "price_asc") return a.price - b.price
      if (sort.value === "price_desc") return b.price - a.price
      return a.duration_minutes - b.duration_minutes
    })
  })

  let debounce: ReturnType<typeof setTimeout>
  function onQuery(v: string) {
    query.value = v
    clearTimeout(debounce)
    if (!v.trim()) {
      svcStore.fetchServices()
      return
    }
    debounce = setTimeout(async () => {
      searching.value = true
      try {
        const payload: any = { q: v }
        if (activeCat.value !== "all") payload.category_id = activeCat.value
        svcStore.services = await searchServices(payload)
      } finally {
        searching.value = false
      }
    }, 400)
  }

  function resetAppliedFilters() {
    query.value = ""
    activeCat.value = "all"
    minPrice.value = null
    maxPrice.value = null
    minRating.value = 0
    maxDistance.value = null
    useLocation.value = false
    svcStore.fetchServices()
  }

  return {
    showFilters,
    query,
    activeCat,
    sort,
    minPrice,
    maxPrice,
    minRating,
    maxDistance,
    useLocation,
    tempActiveCat,
    tempSort,
    tempMinPrice,
    tempMaxPrice,
    tempMinRating,
    tempMaxDistance,
    tempUseLocation,
    locLoading,
    searching,
    filtered,
    onQuery,
    openFilters,
    cancelFilters,
    applyFilters,
    clearFilters,
    toggleLocation,
    resetAppliedFilters,
  }
}
