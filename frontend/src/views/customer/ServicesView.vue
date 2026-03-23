<script setup lang="ts">
import { ref, onMounted } from "vue"

// mock data (replace later with API)
const services = ref<any[]>([])

onMounted(() => {
  // TODO: replace with API call
  services.value = [
    { id: 1, name: "Plumbing Service", lat: 15.144, lng: 120.588 },
    { id: 2, name: "Electrical Repair", lat: 15.146, lng: 120.590 }
  ]
})
</script>

<template>
  <div class="services-map">
    <h1 class="title">Services Map</h1>

    <!-- MAP PLACEHOLDER -->
    <div class="map-container">
      <p>🗺️ Map will go here</p>
    </div>

    <!-- SERVICES LIST -->
    <div class="services-list">
      <div 
        v-for="service in services" 
        :key="service.id" 
        class="service-card"
      >
        <h3>{{ service.name }}</h3>
        <p>Lat: {{ service.lat }}, Lng: {{ service.lng }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.services-map {
  padding: 20px;
  color: white;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 16px;
}

.map-container {
  height: 300px;
  background: #1a1625;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.services-list {
  display: grid;
  gap: 10px;
}

.service-card {
  padding: 12px;
  background: #151226;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
}
</style>