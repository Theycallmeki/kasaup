<script setup lang="ts">
import { onMounted, ref } from "vue"
import L from "leaflet"
import { useUserLocation } from "../hooks/useUserLocation"

const emit = defineEmits(["location-selected"])

const { getSavedLocation } = useUserLocation()

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

let map: any = null
let marker: any = null

const customPin = L.divIcon({
  className: "",
  html: `<div style="width:16px;height:16px;border-radius:50%;background:#38bdf8;box-shadow:0 0 0 4px rgba(56, 189, 248, 0.3);"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8]
})

function updateMap(newLat: number, newLng: number) {
  lat.value = newLat
  lng.value = newLng

  emit("location-selected", {
    latitude: newLat,
    longitude: newLng
  })

  if (map) {
    map.setView([newLat, newLng], 15)
    if (marker) {
      marker.setLatLng([newLat, newLng])
    } else {
      marker = L.marker([newLat, newLng], { icon: customPin }).addTo(map)
    }
  }
}

function useMyLocation() {
  const saved = getSavedLocation()
  if (saved && saved.latitude && saved.longitude) {
    updateMap(saved.latitude, saved.longitude)
    return
  }

  if (!navigator.geolocation) return
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      updateMap(pos.coords.latitude, pos.coords.longitude)
    },
    (err) => {
      console.warn("Location permission denied or unavailable.", err)
    }
  )
}

onMounted(() => {
  const philippinesBounds = L.latLngBounds([4.5, 116.0], [21.5, 127.0])

  map = L.map("picker-map", {
    maxBounds: philippinesBounds,
    minZoom: 6,
    maxZoom: 18,
    attributionControl: false
  }).setView([12.8797, 121.774], 6)

  L.tileLayer("https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png", {
    attribution: '© <a href="https://stadiamaps.com/">Stadia Maps</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    noWrap: true,
  }).addTo(map)

  const customPin = L.divIcon({
    className: "",
    html: `<div style="width:16px;height:16px;border-radius:50%;background:#38bdf8;box-shadow:0 0 0 4px rgba(56, 189, 248, 0.3);"></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  })

  map.on("click", (e: any) => {
    lat.value = e.latlng.lat
    lng.value = e.latlng.lng

    emit("location-selected", {
      latitude: lat.value,
      longitude: lng.value
    })

    if (marker) {
      marker.setLatLng(e.latlng)
    } else {
      marker = L.marker(e.latlng, { icon: customPin }).addTo(map)
    }
  })

  window.setTimeout(() => {
    map?.invalidateSize()
  }, 100)
  window.setTimeout(() => {
    map?.invalidateSize()
    
    useMyLocation()
  }, 400)
})
</script>

<template>
  <div class="location-picker-root">
    <div class="picker-toolbar">
      <button type="button" class="location-btn" @click="useMyLocation">
        Use My Location
      </button>
    </div>
    <div id="picker-map" class="picker-map-el"></div>
    <div v-if="lat !== null && lng !== null" class="coords">
      {{ lat.toFixed(5) }}, {{ lng.toFixed(5) }}
    </div>
  </div>
</template>

<style scoped>
.location-picker-root {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  flex: 1;
}

.picker-toolbar {
  flex-shrink: 0;
  padding: 0 0 8px;
}

.location-btn {
  padding: 8px 14px;
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  background: rgba(124, 58, 237, 0.35);
  color: #fff;
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}
.location-btn:hover {
  background: rgba(124, 58, 237, 0.55);
}

/* Leaflet target — height comes from flex parent; CreateServiceView may override :deep */
.picker-map-el {
  flex: 1;
  min-height: 240px;
  width: 100%;
  border-radius: 10px;
  overflow: hidden;
}

.coords {
  flex-shrink: 0;
  margin-top: 8px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
  font-family: ui-monospace, monospace;
}

.picker-map-el :deep(.leaflet-container) {
  height: 100%;
  min-height: 240px;
  border-radius: 10px;
  background: #1a1a1a;
  filter: saturate(0.8) brightness(1.1);
}
</style>
