<script setup lang="ts">
import { onMounted, watch, ref } from "vue"
import L from "leaflet"

const props = defineProps<{
  show: boolean
  lat: number | null
  lng: number | null
  customerName?: string
}>()

let map: any = null
const mapReady = ref(false)

function initMap() {
  if (!props.lat || !props.lng) return
  const el = document.getElementById("provider-view-map")
  if (!el) return

  if (map) {
    map.remove()
    map = null
  }

  map = L.map("provider-view-map").setView([props.lat, props.lng], 15)

  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    attribution: "© CartoDB",
    noWrap: true
  }).addTo(map)

  const pinIcon = L.divIcon({
    className: "",
    html: `<div class="customer-pin"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9]
  })

  L.marker([props.lat, props.lng], { icon: pinIcon }).addTo(map)

  setTimeout(() => map?.invalidateSize(), 150)
  mapReady.value = true
}

onMounted(() => {
  if (props.show && props.lat && props.lng) {
    setTimeout(initMap, 100)
  }
})

watch(() => [props.show, props.lat, props.lng], ([show]) => {
  if (show) {
    setTimeout(initMap, 100)
  } else {
    mapReady.value = false
  }
})
</script>

<template>
  <Transition name="slide-in">
    <div v-if="show" class="map-sidebar">
      <div class="map-card">
        <div class="map-card-header">
          <svg class="map-pin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <div>
            <h3 class="map-card-title">Customer Location</h3>
            <p class="map-card-desc">
              Home service for
              <strong>{{ customerName || "Customer" }}</strong>
            </p>
          </div>
        </div>

        <div v-if="lat && lng" class="map-wrap">
          <div id="provider-view-map" class="map-el"></div>
        </div>
        <div v-else class="map-empty">
          <span>No location data available</span>
        </div>

        <div v-if="lat && lng" class="map-coords">
          <span class="coord-label">Coordinates</span>
          <span class="coord-val">{{ lat.toFixed(5) }}, {{ lng.toFixed(5) }}</span>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.map-sidebar {
  flex: 1;
  min-width: 0;
  position: sticky;
  top: 36px;
  align-self: flex-start;
  display: flex;
  flex-direction: column;
}

.map-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  box-sizing: border-box;
}

.map-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
}

.map-pin-icon {
  width: 22px;
  height: 22px;
  color: #38bdf8;
  flex-shrink: 0;
  margin-top: 2px;
}

.map-card-title {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem;
  color: #38bdf8;
  margin: 0 0 4px;
}

.map-card-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
  line-height: 1.4;
}

.map-card-desc strong {
  color: rgba(255, 255, 255, 0.8);
}

.map-wrap {
  border-radius: 12px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  background: #0e0c1a;
}

.map-el {
  height: 560px;
  width: 100%;
}

.map-empty {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}

.map-coords {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.coord-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(255, 255, 255, 0.3);
}

.coord-val {
  font-size: 13px;
  font-family: ui-monospace, monospace;
  color: #38bdf8;
  font-weight: 500;
}

/* Transition */
.slide-in-enter-active,
.slide-in-leave-active {
  transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-in-enter-from,
.slide-in-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

@media (max-width: 900px) {
  .map-sidebar {
    width: 100%;
    position: static;
  }
}
</style>

<style>
.customer-pin {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #38bdf8;
  box-shadow: 0 0 0 5px rgba(56, 189, 248, 0.25);
}
</style>
