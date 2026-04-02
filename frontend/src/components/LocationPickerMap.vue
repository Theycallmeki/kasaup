<script setup lang="ts">
import { onMounted, ref } from "vue"
import L from "leaflet"

const emit = defineEmits(["location-selected"])

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

let map: any = null
let marker: any = null

function useMyLocation() {
  if (!navigator.geolocation) return

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const newLat = pos.coords.latitude
      const newLng = pos.coords.longitude

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
          marker = L.marker([newLat, newLng]).addTo(map)
        }
      }
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
    maxZoom: 18
  }).setView([12.8797, 121.774], 6)

  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
    noWrap: true
  }).addTo(map)

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
      marker = L.marker(e.latlng).addTo(map)
    }
  })

  window.setTimeout(() => {
    map?.invalidateSize()
  }, 100)
  window.setTimeout(() => {
    map?.invalidateSize()
    
    // Auto-fetch location if possible
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
