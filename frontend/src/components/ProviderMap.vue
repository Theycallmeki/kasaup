<script setup lang="ts">
import { onMounted, watch, ref } from "vue"
import { useRouter } from "vue-router"
import L from "leaflet"

const props = defineProps<{
  providers: Record<string, unknown>[]
  userLat: number | null
  userLng: number | null
}>()

const router = useRouter()

const mapContainer = ref<any>(null)

let map: any = null
let userMarker: any = null
let pendingUserCoords: { lat: number; lng: number } | null = null
let routeLayer: any = null
let providerMarkersLayer: any = null

function escapeHtml(text: string) {
  const div = document.createElement("div")
  div.textContent = text
  return div.innerHTML
}

function setUserMarker(lat: number, lng: number) {
  if (!map) return

  const userIcon = L.divIcon({
    className: "",
    html: `<div class="kasaup-user-pin"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9]
  })

  if (userMarker) {
    userMarker.setLatLng([lat, lng])
  } else {
    userMarker = L.marker([lat, lng], { icon: userIcon })
      .addTo(map)
      .bindPopup(`<div class="kasaup-popup"><p class="kasaup-popup-name">You are here</p></div>`)
  }

  map.setView([lat, lng], 13, { animate: true })
}

async function drawOptimizedRoute(destinationLat: number, destinationLng: number) {
  const originLat = props.userLat
  const originLng = props.userLng

  if (originLat == null || originLng == null) {
    alert("Please set your location first using 'Use My Location'.")
    return
  }

  if (!map) return

  try {
    const url = `https://router.project-osrm.org/route/v1/driving/${originLng},${originLat};${destinationLng},${destinationLat}?overview=full&geometries=geojson&alternatives=false&steps=false`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`Routing request failed: ${res.status}`)

    const data = (await res.json()) as any
    const route = data?.routes?.[0]
    if (!route?.geometry) throw new Error("No route found")

    if (routeLayer) {
      map.removeLayer(routeLayer)
      routeLayer = null
    }

    routeLayer = L.geoJSON(route.geometry, {
      style: {
        color: "#a78bfa",
        weight: 4,
        opacity: 0.9,
        dashArray: "0"
      }
    }).addTo(map)

    const bounds = routeLayer.getBounds()
    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [24, 24], maxZoom: 16, animate: true })
    }

  } catch (err: any) {
    console.error(err)
    alert(err?.message || "Unable to get directions.")
  }
}

function fitMapToProviders(providers: Record<string, unknown>[]) {
  if (!map) return
  if (!providers.length) {
    map.setView([12.8797, 121.774], 6, { animate: true })
    return
  }
  const valid = providers.filter(
    (p) => typeof p.latitude === "number" && typeof p.longitude === "number"
  ) as { latitude: number; longitude: number }[]
  if (!valid.length) return
  try {
    const bounds = L.latLngBounds(valid.map((p) => [p.latitude, p.longitude]))
    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [48, 48], maxZoom: 13, animate: true })
    }
  } catch (e) {
    console.warn("fitBounds failed", e)
  }
}

function refreshProviderMarkers() {
  if (!map) return

  if (providerMarkersLayer) {
    map.removeLayer(providerMarkersLayer)
    providerMarkersLayer = null
  }

  providerMarkersLayer = L.layerGroup()

  for (const provider of props.providers) {
    const lat = provider.latitude
    const lng = provider.longitude
    if (typeof lat !== "number" || typeof lng !== "number") continue

    const id = provider.id
    const name = typeof provider.shop_name === "string" ? provider.shop_name : "Provider"
    const dist =
      typeof provider.distance_km === "number"
        ? `<p class="kasaup-popup-sub">${provider.distance_km.toFixed(1)} km away</p>`
        : ""

    const providerIcon = L.divIcon({
      className: "",
      html: `<div class="kasaup-provider-pin"></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    })

    const marker = L.marker([lat, lng], { icon: providerIcon })

    const popupDiv = document.createElement("div")
    popupDiv.className = "kasaup-popup"

    popupDiv.innerHTML = `
      <p class="kasaup-popup-name">${escapeHtml(name)}</p>
      ${dist}
      <div class="kasaup-popup-btns">
        <button class="kasaup-popup-btn kasaup-btn-view" id="view-${id}">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          View
        </button>
        <button class="kasaup-popup-btn kasaup-btn-dir" id="dir-${id}">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
          Directions
        </button>
      </div>
    `

    marker.bindPopup(popupDiv, {
      className: "kasaup-leaflet-popup",
      maxWidth: 220,
      minWidth: 180
    })

    marker.on("popupopen", () => {
      document.getElementById(`view-${id}`)?.addEventListener("click", () => {
        router.push(`/providers/${id}`)
      })
      document.getElementById(`dir-${id}`)?.addEventListener("click", () => {
        drawOptimizedRoute(lat, lng)
      })
    })

    providerMarkersLayer.addLayer(marker)
  }

  providerMarkersLayer.addTo(map)
}

onMounted(() => {
  const philippinesBounds = L.latLngBounds([4.5, 116.0], [21.5, 127.0])

  map = L.map(mapContainer.value, {
    maxBounds: philippinesBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 6,
    maxZoom: 18,
    worldCopyJump: false,
    zoomControl: true,
    zoomAnimation: true,
    fadeAnimation: true,
    markerZoomAnimation: true,
    preferCanvas: true
  }).setView([12.8797, 121.774], 6)

  L.tileLayer("https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png", {
    attribution: '© <a href="https://stadiamaps.com/">Stadia Maps</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    noWrap: true,
    keepBuffer: 8,
    updateWhenZooming: false,
    updateWhenIdle: true
  }).addTo(map)

  refreshProviderMarkers()
  fitMapToProviders(props.providers)

  map.setMaxBounds(philippinesBounds)

  if (pendingUserCoords) {
    setUserMarker(pendingUserCoords.lat, pendingUserCoords.lng)
  }

  setTimeout(() => map.invalidateSize(), 200)
})

watch(
  () => props.providers,
  (providers) => {
    refreshProviderMarkers()
    fitMapToProviders(providers)
  }
)

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
  <div ref="mapContainer" class="map" />
</template>

<style scoped>
.map {
  height: 100vh;
  width: 100%;
  background: #0e0c1a;
  transform: translateZ(0);
  will-change: transform;
}
</style>

<style>
.leaflet-container {
  background: #0e0c1a;
  transform: translateZ(0);
}

.kasaup-provider-pin {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #a78bfa;
  box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.25);
}

.kasaup-user-pin {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 0 5px rgba(52, 211, 153, 0.25);
}

.kasaup-leaflet-popup .leaflet-popup-content-wrapper {
  background: #13111f;
  border: 1px solid rgba(167, 139, 250, 0.2);
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  padding: 0;
}
.kasaup-leaflet-popup .leaflet-popup-content {
  margin: 0;
}
.kasaup-leaflet-popup .leaflet-popup-tip-container {
  display: none;
}
.kasaup-popup {
  padding: 14px 16px;
  font-family: 'DM Sans', sans-serif;
}
.kasaup-popup-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
}
.kasaup-popup-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0 0 14px;
}
.kasaup-popup-btns {
  display: flex;
  gap: 7px;
}
.kasaup-popup-btn {
  flex: 1;
  padding: 8px 10px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: opacity 0.15s;
}
.kasaup-popup-btn:hover {
  opacity: 0.85;
}
.kasaup-btn-view {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
}
.kasaup-btn-dir {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
}
</style>