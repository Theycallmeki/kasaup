<script setup lang="ts">
import { onMounted } from "vue"
import L from "leaflet"
import { useProviderStore } from "../stores/providerStore"

const providerStore = useProviderStore()

onMounted(async () => {

  await providerStore.fetchProviders()

  const map = L.map("map").setView([14.5995, 120.9842], 12)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
  }).addTo(map)

  providerStore.providers.forEach((provider: any) => {

    if (!provider.latitude || !provider.longitude) return

    L.marker([provider.latitude, provider.longitude])
      .addTo(map)
      .bindPopup(provider.shop_name)

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