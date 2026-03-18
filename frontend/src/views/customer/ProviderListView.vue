<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useProviderStore } from "../../stores/providerStore"
import ProviderMap from "../../components/ProviderMap.vue"

const providerStore = useProviderStore()

const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)

const USER_LOCATION_KEY = "kasaup:user_location_v1"

function persistUserLocation(lat: number, lng: number) {
  try {
    localStorage.setItem(
      USER_LOCATION_KEY,
      JSON.stringify({ lat, lng })
    )
  } catch (e) {
    // If storage is blocked, just skip persistence.
    // eslint-disable-next-line no-console
    console.warn("Unable to persist user location:", e)
  }
}

function restoreUserLocation() {
  try {
    const raw = localStorage.getItem(USER_LOCATION_KEY)
    if (!raw) return

    const parsed = JSON.parse(raw) as { lat?: unknown; lng?: unknown }
    if (typeof parsed.lat === "number" && typeof parsed.lng === "number") {
      userLat.value = parsed.lat
      userLng.value = parsed.lng
    }
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn("Unable to restore user location:", e)
  }
}

function haversine(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371

  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) *
    Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

  return R * c
}

function useMyLocation() {
  if (!navigator.geolocation) {
    // eslint-disable-next-line no-alert
    alert("Geolocation is not supported by your browser.")
    return
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat.value = pos.coords.latitude
      userLng.value = pos.coords.longitude
      persistUserLocation(userLat.value, userLng.value)

      providerStore.providers = providerStore.providers
        .map((p: any) => {
          if (p.latitude && p.longitude) {
            return {
              ...p,
              distance_km: haversine(
                userLat.value!,
                userLng.value!,
                p.latitude,
                p.longitude
              )
            }
          }
          return p
        })
        .sort((a: any, b: any) => (a.distance_km || 9999) - (b.distance_km || 9999))
    },
    (err) => {
      // Helps diagnose why the button “does nothing” (permission denied, insecure context, etc.)
      // eslint-disable-next-line no-console
      console.error("Geolocation error:", err)
      // eslint-disable-next-line no-alert
      alert(err.message || "Unable to get your location.")
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
  )
}

onMounted(async () => {
  restoreUserLocation()
  await providerStore.fetchProviders()
})
</script>

<template>

<div class="providers-page">

  <div class="search-bar">
    <input placeholder="Search services or providers..." />
    <button @click="useMyLocation">Use My Location</button>
  </div>

  <ProviderMap
    :providers="providerStore.providers"
    :userLat="userLat"
    :userLng="userLng"
  />

</div>

</template>

<style scoped>

.providers-page{
position:relative;
height:100vh;
width:100%;
}

.search-bar{
position:absolute;
top:20px;
left:50%;
transform:translateX(-50%);
z-index:1000;
width:420px;
display:flex;
gap:8px;
}

.search-bar input{
flex:1;
padding:12px 16px;
border-radius:10px;
border:1px solid #cbd5e1;
box-shadow:0 5px 15px rgba(0,0,0,0.15);
font-size:14px;
}

.search-bar button{
padding:12px;
border:none;
border-radius:10px;
background:#16a34a;
color:white;
cursor:pointer;
}

.search-bar button:hover{
background:#15803d;
}

</style>