<script setup lang="ts">
import { onMounted, watch, ref } from "vue"
import { useRouter } from "vue-router"
import L from "leaflet"
import api from "../services/api"

const props = defineProps<{
  providers: Record<string, unknown>[]
  userLat: number | null
  userLng: number | null
}>()

const router = useRouter()

const mapContainer = ref<any>(null)
const activeDirections = ref<Record<string, unknown> | null>(null)

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

  userMarker = L.marker([lat, lng], { icon: userIcon })
    .addTo(map)
    .bindPopup(`<div class="kasaup-popup"><p class="kasaup-popup-name">You are here</p></div>`, {
      className: "kasaup-leaflet-popup"
    })

  map.setView([lat, lng], 13, { animate: true })
}

async function drawOptimizedRoute(provider: Record<string, unknown>) {
  const destinationLat = provider.latitude as number
  const destinationLng = provider.longitude as number
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

    activeDirections.value = provider
    refreshProviderMarkers()

  } catch (err: any) {
    console.error(err)
    alert(err?.message || "Unable to get directions.")
  }
}

function cancelDirections() {
  activeDirections.value = null

  if (routeLayer) {
    map.removeLayer(routeLayer)
    routeLayer = null
  }

  refreshProviderMarkers()
  fitMapToProviders(props.providers)
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

  const visibleProviders = activeDirections.value
    ? props.providers.filter(p => p.id === activeDirections.value!.id)
    : props.providers

  for (const provider of visibleProviders) {
    const lat = provider.latitude
    const lng = provider.longitude
    if (typeof lat !== "number" || typeof lng !== "number") continue

    const id = provider.id
    const name = typeof provider.shop_name === "string" ? provider.shop_name : "Provider"
    const dist =
      typeof provider.distance_km === "number"
        ? `<div class="kasaup-popup-sub"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg><span>${provider.distance_km.toFixed(1)} km away</span></div>`
        : ""

    const rawImage = typeof provider.profile_image === "string" ? provider.profile_image : null
    const imgFullUrl = rawImage
      ? (rawImage.startsWith("http") ? rawImage : `${api.defaults.baseURL}/${rawImage.replace(/^\//, "")}`)
      : null
      
    const initials = name.split(" ").map((w: string) => w[0]).join("").slice(0, 2).toUpperCase()
    const avatarHTML = imgFullUrl
      ? `<img src="${imgFullUrl}" class="kasaup-popup-avatar kasaup-popup-avatar--img" alt="${escapeHtml(name)}" />`
      : `<div class="kasaup-popup-avatar kasaup-popup-avatar--initials">${escapeHtml(initials)}</div>`

    const providerIcon = L.divIcon({
      className: "",
      html: `<div class="kasaup-provider-pin${activeDirections.value ? ' kasaup-provider-pin--active' : ''}"></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    })

    const marker = L.marker([lat, lng], { icon: providerIcon })

    const popupDiv = document.createElement("div")
    popupDiv.className = "kasaup-popup"

    popupDiv.innerHTML = `
      <div class="kasaup-popup-header">
        ${avatarHTML}
        <div class="kasaup-popup-header-info">
          <h3 class="kasaup-popup-name">${escapeHtml(name)}</h3>
          ${dist}
        </div>
      </div>
      <div class="kasaup-popup-btns">
        <button class="kasaup-popup-btn kasaup-btn-view" id="view-${id}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          View
        </button>
        <button class="kasaup-popup-btn kasaup-btn-dir" id="dir-${id}">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
          Directions
        </button>
      </div>
    `

    marker.bindPopup(popupDiv, {
      className: "kasaup-leaflet-popup",
      maxWidth: 240,
      minWidth: 200
    })

    marker.on("popupopen", () => {
      document.getElementById(`view-${id}`)?.addEventListener("click", () => {
        router.push(`/providers/${id}`)
      })
      document.getElementById(`dir-${id}`)?.addEventListener("click", () => {
        drawOptimizedRoute(provider)
      })
    })

    providerMarkersLayer.addLayer(marker)
  }

  providerMarkersLayer.addTo(map)
}

onMounted(() => {
  const philippinesBounds = L.latLngBounds([4.5, 116.0], [21.5, 127.0])

  map = L.map(mapContainer.value, {
    attributionControl: false,
    maxBounds: philippinesBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 6,
    maxZoom: 18,
    worldCopyJump: false,
    zoomControl: false,
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
    if (!activeDirections.value) fitMapToProviders(providers)
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
  <div class="map-root">
    <div ref="mapContainer" class="map" />

    <Transition name="cancel-btn">
      <div v-if="activeDirections" class="cancel-directions-bar">
        <div class="cancel-directions-inner">
          <div class="cancel-info">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="3 11 22 2 13 21 11 13 3 11"/>
            </svg>
            <span>Directions to <strong>{{ activeDirections.shop_name }}</strong></span>
          </div>
          <button class="cancel-btn" @click="cancelDirections">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancel
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.map-root {
  position: relative;
  height: 100vh;
  width: 100%;
}

.map {
  height: 100%;
  width: 100%;
  background: #0e0c1a;
  transform: translateZ(0);
  will-change: transform;
}

.cancel-directions-bar {
  position: absolute;
  top: 90px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  pointer-events: all;
}

@media (max-width: 600px) {
  .cancel-directions-bar {
    top: 130px;
    width: calc(100% - 32px);
  }
  .cancel-directions-inner {
    width: 100%;
    box-sizing: border-box;
    justify-content: space-between;
  }
  .cancel-info {
    min-width: 0;
  }
  .cancel-info span {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: block;
  }
}

.cancel-directions-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #13111f;
  border: 1px solid rgba(167, 139, 250, 0.35);
  border-radius: 12px;
  padding: 10px 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  font-family: 'DM Sans', sans-serif;
  white-space: nowrap;
}

.cancel-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.cancel-info svg { color: #a78bfa; flex-shrink: 0; }
.cancel-info strong { color: #fff; font-weight: 600; }

.cancel-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(248, 113, 113, 0.1);
  border: 0.5px solid rgba(248, 113, 113, 0.3);
  border-radius: 8px;
  color: #f87171;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}
.cancel-btn:hover { background: rgba(248, 113, 113, 0.18); }

.cancel-btn-enter-active,
.cancel-btn-leave-active {
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.cancel-btn-enter-from,
.cancel-btn-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-8px);
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

.kasaup-provider-pin--active {
  background: #38bdf8;
  box-shadow: 0 0 0 5px rgba(56, 189, 248, 0.3);
}

.kasaup-user-pin {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 0 5px rgba(52, 211, 153, 0.25);
}

.kasaup-leaflet-popup .leaflet-popup-content-wrapper {
  background: rgba(18, 16, 30, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(255, 255, 255, 0.02);
  padding: 0;
}
.kasaup-leaflet-popup .leaflet-popup-content {
  margin: 0;
}
.kasaup-leaflet-popup .leaflet-popup-tip-container {
  display: none;
}
.kasaup-leaflet-popup .leaflet-popup-close-button {
  display: none !important;
}

/* Popup layout */
.kasaup-popup {
  padding: 18px;
  font-family: 'DM Sans', sans-serif;
}

.kasaup-popup-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.kasaup-popup-header-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  justify-content: center;
}

.kasaup-popup-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.25);
  background: #1a1829;
}

.kasaup-popup-avatar--img {
  object-fit: cover;
  border: none;
}

.kasaup-popup-avatar--initials {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(167, 139, 250, 0.08));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #c4b5fd;
  font-family: 'Sora', sans-serif;
}

.kasaup-popup-name {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: 0.2px;
  line-height: 1.2;
}

.kasaup-popup-sub {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
  line-height: 1;
}
.kasaup-popup-sub svg {
  color: rgba(167, 139, 250, 0.8);
}

.kasaup-popup-btns {
  display: flex;
  gap: 8px;
}
.kasaup-popup-btn {
  flex: 1;
  padding: 10px 12px;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.kasaup-popup-btn:active {
  transform: scale(0.96);
}
.kasaup-btn-view {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
}
.kasaup-btn-view:hover {
  background: linear-gradient(135deg, #8b5cf6, #b165f8);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
  transform: translateY(-1px);
}
.kasaup-btn-dir {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}
.kasaup-btn-dir:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}
</style>