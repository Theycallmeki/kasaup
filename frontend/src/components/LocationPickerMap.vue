<script setup lang="ts">
import { onMounted, ref } from "vue"
import L from "leaflet"

const emit = defineEmits(["location-selected"])

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

let map: any = null
let marker: any = null

function useMyLocation() {
  navigator.geolocation.getCurrentPosition((pos) => {
    const newLat = pos.coords.latitude
    const newLng = pos.coords.longitude

    lat.value = newLat
    lng.value = newLng

    emit("location-selected", {
      latitude: newLat,
      longitude: newLng
    })

    map.setView([newLat, newLng], 15)

    if (marker) {
      marker.setLatLng([newLat, newLng])
    } else {
      marker = L.marker([newLat, newLng]).addTo(map)
    }
  })
}

onMounted(() => {

  const philippinesBounds = L.latLngBounds(
    [4.5, 116.0],
    [21.5, 127.0]
  )

  map = L.map("picker-map", {
    maxBounds: philippinesBounds,
    minZoom: 6,
    maxZoom: 18
  }).setView([12.8797, 121.7740], 6)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
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

})
</script>

<template>

<div class="location-picker">

  <button @click="useMyLocation">
    Use My Location
  </button>

  <div id="picker-map"></div>

  <div class="coords" v-if="lat !== null && lng !== null">
    Latitude: {{ lat }} <br />
    Longitude: {{ lng }}
  </div>

</div>

</template>

<style scoped>

#picker-map{
  height:400px;
  width:100%;
  border-radius:10px;
  margin-top:10px;
}

.coords{
  margin-top:10px;
  font-size:14px;
}

button{
  padding:8px 12px;
  border:none;
  border-radius:6px;
  background:#2563eb;
  color:white;
  cursor:pointer;
}

button:hover{
  background:#1d4ed8;
}

</style>