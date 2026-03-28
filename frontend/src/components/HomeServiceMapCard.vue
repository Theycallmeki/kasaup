<script setup lang="ts">
import LocationPickerMap from "./LocationPickerMap.vue"

defineProps<{
  show: boolean
  customerLat: number | null
  customerLng: number | null
}>()

const emit = defineEmits(["location-selected"])

function setLocation(data: any) {
  emit("location-selected", data)
}
</script>

<template>
  <div class="profile-sidebar" v-if="show">
    <div class="map-card">
      <div class="map-card-header">
        <svg class="map-pin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
        <div>
          <h3 class="map-card-title">Pin Location</h3>
          <p class="map-card-desc">Move the map to set your exact home service address.</p>
        </div>
      </div>
      
      <div class="location-map">
        <LocationPickerMap @location-selected="setLocation" />
      </div>
      
      <div class="map-card-footer" v-if="customerLat && customerLng">
        <span class="coord-label">Selected Coordinates:</span>
        <span class="coords-hint">{{ customerLat.toFixed(5) }}, {{ customerLng.toFixed(5) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-sidebar {
  width: 800px;
  flex-shrink: 0;
  position: sticky;
  top: 36px;
  animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.map-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(167, 139, 250, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.map-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
}

.map-pin-icon {
  width: 20px;
  height: 20px;
  color: #c4b5fd;
  flex-shrink: 0;
  margin-top: 2px;
}

.map-card-title {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem;
  color: #c4b5fd;
  margin: 0 0 6px;
}

.map-card-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 20px;
  line-height: 1.4;
}

.location-map {
  border-radius: 12px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  height: 600px;
  background: #0e0c1a;
}

.map-card-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.coord-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.3);
}

.coords-hint {
  font-size: 13px;
  font-family: ui-monospace, monospace;
  color: #38bdf8;
  font-weight: 500;
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

@media (max-width: 900px) {
  .profile-sidebar {
    width: 100%;
    position: static;
  }
}
</style>
