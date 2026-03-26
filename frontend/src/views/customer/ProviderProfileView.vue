<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import { useAppointmentStore } from "../../stores/appointmentStore"
import LocationPickerMap from "../../components/LocationPickerMap.vue"
import api from "../../services/api"

const route = useRoute()
const providerStore = useProviderStore()
const appointmentStore = useAppointmentStore()

const id = Number(route.params.id)

const activeServiceId = ref<number | null>(null)
const customerLat = ref<number | null>(null)
const customerLng = ref<number | null>(null)

const imgUrl = (path: string) => `${api.defaults.baseURL}/${path}`

onMounted(async () => {
  await providerStore.fetchProviderProfile(id)
})

async function loadSlots(serviceId: number) {
  activeServiceId.value = serviceId
  await appointmentStore.fetchAvailableSlots(serviceId)
}

function setLocation(data: any) {
  customerLat.value = data.latitude
  customerLng.value = data.longitude
}

async function book(serviceId: number, slot: string) {
  await appointmentStore.bookAppointment({
    provider_id: id,
    service_id: serviceId,
    appointment_time: slot,
    customer_latitude: customerLat.value,
    customer_longitude: customerLng.value
  })
  appointmentStore.slots = []
  activeServiceId.value = null
  customerLat.value = null
  customerLng.value = null
}

const formatSlot = (iso: string) =>
  new Date(iso).toLocaleString("en-PH", {
    weekday: "short", month: "short", day: "numeric",
    hour: "numeric", minute: "2-digit"
  })
</script>

<template>
  <div class="page">

    <div v-if="providerStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
      </svg>
      Loading provider...
    </div>

    <template v-else-if="providerStore.providerProfile">

      <div class="provider-header">
        <div class="provider-avatar">
          {{ providerStore.providerProfile.provider.shop_name?.charAt(0) }}
        </div>
        <div>
          <h1 class="provider-name">{{ providerStore.providerProfile.provider.shop_name }}</h1>
          <p class="provider-desc">{{ providerStore.providerProfile.provider.description }}</p>
          <div v-if="providerStore.providerProfile.provider.offers_home_service" class="home-badge">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
            Offers Home Service
          </div>
        </div>
      </div>

      <div class="divider" />

      <h2 class="section-title">Services</h2>

      <div class="services">
        <div
          v-for="service in providerStore.providerProfile.services"
          :key="service.id"
          class="service-card"
          :class="{ 'service-active': activeServiceId === service.id }"
        >

          <div v-if="service.images?.length" class="service-images">
            <img
              v-for="img in service.images"
              :key="img.id"
              :src="imgUrl(img.image_url)"
              class="service-img"
              alt=""
            />
          </div>

          <div class="service-top">
            <div>
              <div class="service-name">{{ service.name }}</div>
              <div class="service-meta">
                <span class="meta-pill">₱{{ service.price }}</span>
                <span class="meta-pill">{{ service.duration_minutes }} min</span>
              </div>
            </div>
            <button
              class="book-btn"
              :class="{ 'book-btn-active': activeServiceId === service.id }"
              @click="loadSlots(service.id)"
            >
              {{ activeServiceId === service.id ? 'Viewing slots' : 'Book' }}
            </button>
          </div>

          <template v-if="activeServiceId === service.id && appointmentStore.slots.length">

            <div
              v-if="providerStore.providerProfile.provider.offers_home_service"
              class="location-section"
            >
              <div class="location-label">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
                </svg>
                Set your location for home service
              </div>
              <div class="location-map">
                <LocationPickerMap @location-selected="setLocation" />
              </div>
              <p v-if="customerLat && customerLng" class="coords-hint">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
                </svg>
                {{ customerLat.toFixed(4) }}, {{ customerLng.toFixed(4) }}
              </p>
            </div>

            <div class="slots-label">Available slots</div>
            <div class="slots">
              <div
                v-for="slot in appointmentStore.slots"
                :key="slot"
                class="slot"
              >
                <span class="slot-time">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                  </svg>
                  {{ formatSlot(slot) }}
                </span>
                <button class="confirm-btn" @click="book(service.id, slot)">
                  Confirm
                </button>
              </div>
            </div>

          </template>
        </div>
      </div>

    </template>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
  max-width: 720px;
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: rgba(255,255,255,0.3);
  font-size: 14px;
  gap: 8px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; }

.provider-header {
  display: flex;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 28px;
}

.provider-avatar {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(99, 60, 220, 0.25);
  border: 0.5px solid rgba(130, 90, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #a78bfa;
  flex-shrink: 0;
}

.provider-name {
  font-family: 'Sora', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
}

.provider-desc {
  font-size: 14px;
  color: rgba(255,255,255,0.4);
  margin: 0 0 10px;
  line-height: 1.5;
}

.home-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(52, 211, 153, 0.8);
  background: rgba(52, 211, 153, 0.1);
  border: 0.5px solid rgba(52, 211, 153, 0.25);
  border-radius: 100px;
  padding: 3px 10px;
}

.divider {
  height: 0.5px;
  background: rgba(255,255,255,0.07);
  margin-bottom: 28px;
}

.section-title {
  font-family: 'Sora', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px;
}

.services {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.service-card {
  background: rgba(255,255,255,0.035);
  border: 0.5px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.service-active {
  border-color: rgba(167, 139, 250, 0.3);
}

.service-images {
  display: flex;
  overflow-x: auto;
  scrollbar-width: none;
}
.service-images::-webkit-scrollbar { display: none; }

.service-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  flex-shrink: 0;
  display: block;
}

.service-images .service-img:only-child {
  width: 100%;
}

.service-images:not(:has(.service-img:only-child)) .service-img {
  width: 260px;
}

.service-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 18px 0;
}

.service-name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 8px;
}

.service-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  padding-bottom: 16px;
}

.meta-pill {
  font-size: 12px;
  color: rgba(167, 139, 250, 0.8);
  background: rgba(99, 60, 220, 0.15);
  border: 0.5px solid rgba(130, 90, 255, 0.2);
  border-radius: 100px;
  padding: 3px 10px;
}

.book-btn {
  flex-shrink: 0;
  padding: 8px 18px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  transition: opacity 0.15s;
  white-space: nowrap;
}
.book-btn:hover { opacity: 0.85; }
.book-btn-active {
  background: rgba(167, 139, 250, 0.15);
  border: 0.5px solid rgba(167, 139, 250, 0.3);
  color: #a78bfa;
}

.location-section {
  margin: 0 18px;
  padding-top: 16px;
  border-top: 0.5px solid rgba(255,255,255,0.07);
}

.location-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.3);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

.location-map {
  border-radius: 12px;
  overflow: hidden;
  border: 0.5px solid rgba(255,255,255,0.08);
  height: 200px;
}

.coords-hint {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: rgba(167, 139, 250, 0.7);
  margin-top: 8px;
}

.slots-label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.25);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin: 18px 18px 10px;
  padding-top: 16px;
  border-top: 0.5px solid rgba(255,255,255,0.07);
}

.slots {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 0 18px 18px;
}

.slot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(255,255,255,0.03);
  border: 0.5px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  gap: 12px;
}

.slot-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255,255,255,0.6);
}

.confirm-btn {
  flex-shrink: 0;
  padding: 6px 14px;
  border-radius: 7px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  background: rgba(52, 211, 153, 0.12);
  border: 0.5px solid rgba(52, 211, 153, 0.3);
  color: #34d399;
  transition: opacity 0.15s;
}
.confirm-btn:hover { opacity: 0.8; }

@media (max-width: 540px) {
  .page { padding: 24px 16px; }
  .provider-header { flex-direction: column; }
}
</style>