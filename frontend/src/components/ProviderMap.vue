<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import L from "leaflet"
import { useProviderStore } from "../stores/providerStore"

const providerStore = useProviderStore()
const router = useRouter()

onMounted(async () => {

  await providerStore.fetchProviders()

  const philippinesBounds = L.latLngBounds(
    [4.5, 116.0],
    [21.5, 127.0]
  )

  const map = L.map("map", {
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

    const popup = `
      <div>
        <strong>${provider.shop_name}</strong><br/>
        <button id="view-${provider.id}">View Profile</button>
      </div>
    `

    marker.bindPopup(popup)

    marker.on("popupopen", () => {
      const btn = document.getElementById(`view-${provider.id}`)
      if (btn) {
        btn.onclick = () => {
          router.push(`/providers/${provider.id}`)
        }
      }
    })

  })

  map.setMaxBounds(philippinesBounds)

  setTimeout(() => {
    map.invalidateSize()
  }, 200)

})
</script>

<template>
<div id="map"></div>
</template>

<style scoped>

#map{
  height:100vh;
  width:100%;
}

</style>