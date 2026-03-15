<script setup lang="ts">
import { onMounted, ref } from "vue"
import L from "leaflet"

const emit = defineEmits(["location-selected"])

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

onMounted(() => {

  const philippinesBounds = L.latLngBounds(
    [4.5, 116.0],
    [21.5, 127.0]
  )

  const map = L.map("picker-map", {
    maxBounds: philippinesBounds,
    minZoom: 6,
    maxZoom: 18
  }).setView([12.8797, 121.7740], 6)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    noWrap: true
  }).addTo(map)

  let marker: any = null

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

  <div id="picker-map"></div>

  <div class="coords" v-if="lat && lng">
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
}

.coords{
  margin-top:10px;
  font-size:14px;
}

</style>