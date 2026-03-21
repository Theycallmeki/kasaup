<script setup lang="ts">
import { onMounted, watch, ref } from "vue"
import { useRouter } from "vue-router"
import L from "leaflet"
import { useProviderStore } from "../stores/providerStore"

const props = defineProps<{
  userLat: number | null
  userLng: number | null
}>()

const providerStore = useProviderStore()
const router = useRouter()

const mapContainer = ref<any>(null)

let map: any = null
let userMarker: any = null
let pendingUserCoords: { lat: number; lng: number } | null = null
let routeLayer: any = null

function setUserMarker(lat: number, lng: number) {
  if (!map) return

  const userIcon = L.icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32]
  })

  if (userMarker) {
    userMarker.setLatLng([lat, lng])
  } else {
    userMarker = L.marker([lat, lng], { icon: userIcon })
      .addTo(map)
      .bindPopup("You are here")
  }

  map.setView([lat, lng], 13)
}

async function drawOptimizedRoute(
  destinationLat: number,
  destinationLng: number
) {
  const originLat = props.userLat
  const originLng = props.userLng

  if (originLat == null || originLng == null) {
    // eslint-disable-next-line no-alert
    alert("Please set your location first using 'Use My Location'.")
    return
  }

  if (!map) return

  try {
    // OSRM expects coordinates as `lon,lat`.
    const lon1 = originLng
    const lat1 = originLat
    const lon2 = destinationLng
    const lat2 = destinationLat

    const url = `https://router.project-osrm.org/route/v1/driving/${lon1},${lat1};${lon2},${lat2}?overview=full&geometries=geojson&alternatives=false&steps=false`

    const res = await fetch(url)
    if (!res.ok) {
      throw new Error(`Routing request failed: ${res.status}`)
    }

    const data = (await res.json()) as any
    const route = data?.routes?.[0]
    if (!route?.geometry) {
      throw new Error("No route found")
    }

    // Clear previous route
    if (routeLayer) {
      map.removeLayer(routeLayer)
      routeLayer = null
    }

    routeLayer = L.geoJSON(route.geometry, {
      style: {
        color: "#2563eb",
        weight: 5,
        opacity: 0.85
      }
    }).addTo(map)

    const bounds = routeLayer.getBounds()
    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [24, 24], maxZoom: 16 })
    }

    // Provide quick feedback (optional; keeps UI simple)
    const distanceKm = route.distance ? route.distance / 1000 : null
    const durationMin = route.duration ? route.duration / 60 : null
    // eslint-disable-next-line no-console
    console.log("Route:", { distanceKm, durationMin })

  } catch (err: any) {
    // eslint-disable-next-line no-console
    console.error(err)
    // eslint-disable-next-line no-alert
    alert(err?.message || "Unable to get directions.")
  }
}

onMounted(async () => {

  await providerStore.fetchProviders()

  const philippinesBounds = L.latLngBounds(
    [4.5, 116.0],
    [21.5, 127.0]
  )

  map = L.map(mapContainer.value, {
    maxBounds: philippinesBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 6,
    maxZoom: 18,
    worldCopyJump: false,
    zoomControl: true
  }).setView([12.8797, 121.7740], 6)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    noWrap: true
  }).addTo(map)

  providerStore.providers.forEach((provider: any) => {

    if (!provider.latitude || !provider.longitude) return

    const marker = L.marker([provider.latitude, provider.longitude]).addTo(map)

    const popupDiv = document.createElement("div")

    const title = document.createElement("strong")
    title.innerText = provider.shop_name

    const br = document.createElement("br")

    const btn = document.createElement("button")
    btn.innerText = "View Profile"
    btn.onclick = () => {
      router.push(`/providers/${provider.id}`)
    }

    const dirBtn = document.createElement("button")
    dirBtn.innerText = "Directions"
    dirBtn.style.marginLeft = "8px"
    dirBtn.onclick = () => {
      drawOptimizedRoute(provider.latitude, provider.longitude)
    }

    popupDiv.appendChild(title)
    popupDiv.appendChild(br)
    popupDiv.appendChild(btn)
    popupDiv.appendChild(dirBtn)

    marker.bindPopup(popupDiv)

  })

  map.setMaxBounds(philippinesBounds)

  // If the user clicked "Use My Location" before the map was ready,
  // apply the latest coords now that `map` exists.
  if (pendingUserCoords) {
    setUserMarker(pendingUserCoords.lat, pendingUserCoords.lng)
  }

  setTimeout(() => {
    map.invalidateSize()
  }, 200)

})

watch(
  () => [props.userLat, props.userLng],
  ([lat, lng]) => {
    if (lat == null || lng == null) return

    pendingUserCoords = { lat, lng }
    setUserMarker(lat, lng)
  },
  { immediate: true }
)
</script>

<template>
  <div ref="mapContainer" class="map"></div>
</template>

<style scoped>
.map{
  height:100vh;
  width:100%;
}
</style>