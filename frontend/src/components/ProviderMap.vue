<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import L from "leaflet"
import { useProviderStore } from "../stores/providerStore"

const providerStore = useProviderStore()
const router = useRouter()

onMounted(async () => {

  await providerStore.fetchProviders()

  const map = L.map("map").setView([14.5995, 120.9842], 12)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
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

})
</script>

<template>
<div id="map"></div>
</template>

<style scoped>

#map{
  height:500px;
  width:100%;
  border-radius:10px;
}

</style>