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

const loadingSlots = ref(false)
const bookingLoading = ref(false)
const errorMsg = ref("")

const imgUrl = (path: string) =>
  path ? `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}` : ""

onMounted(async () => {
  try {
    await providerStore.fetchProviderProfile(id)
  } catch (e) {
    errorMsg.value = "Failed to load provider."
  }
})

async function loadSlots(serviceId: number) {
  activeServiceId.value = serviceId
  loadingSlots.value = true
  errorMsg.value = ""

  try {
    await appointmentStore.fetchAvailableSlots(serviceId)
  } catch (e) {
    errorMsg.value = "Failed to load available slots."
  } finally {
    loadingSlots.value = false
  }
}

function setLocation(data: any) {
  customerLat.value = data.latitude
  customerLng.value = data.longitude
}

async function book(serviceId: number, slot: string) {
  bookingLoading.value = true
  errorMsg.value = ""

  try {
    await appointmentStore.bookAppointment({
      provider_id: id,
      service_id: serviceId,
      appointment_time: slot,
      customer_latitude: customerLat.value,
      customer_longitude: customerLng.value
    })

    activeServiceId.value = null
    customerLat.value = null
    customerLng.value = null

    await appointmentStore.fetchAvailableSlots(serviceId)

  } catch (e) {
    errorMsg.value = "Booking failed. Try again."
  } finally {
    bookingLoading.value = false
  }
}

const formatSlot = (iso: string) =>
  new Date(iso).toLocaleString("en-PH", {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  })
</script>

<template>
  <div class="page">

    <div v-if="providerStore.loading" class="state-msg">
      <div class="spin">Loading provider...</div>
    </div>

    <div v-else-if="errorMsg" class="state-msg">
      {{ errorMsg }}
    </div>

    <div v-else-if="!providerStore.providerProfile" class="state-msg">
      Provider not found.
    </div>

    <template v-else>

      <div class="provider-header">
        <div class="provider-avatar">
          {{ providerStore.providerProfile.provider.shop_name?.charAt(0) }}
        </div>
        <div>
          <h1 class="provider-name">
            {{ providerStore.providerProfile.provider.shop_name }}
          </h1>
          <p class="provider-desc">
            {{ providerStore.providerProfile.provider.description }}
          </p>

          <div
            v-if="providerStore.providerProfile.provider.offers_home_service"
            class="home-badge"
          >
            Offers Home Service
          </div>
        </div>
      </div>

      <div class="divider" />

      <h2 class="section-title">Services</h2>

      <div
        v-if="!providerStore.providerProfile.services.length"
        class="state-msg"
      >
        No services available.
      </div>

      <div v-else class="services">
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

          <template v-if="activeServiceId === service.id">

            <div v-if="loadingSlots" class="state-msg">
              Loading available slots...
            </div>

            <div
              v-else-if="!appointmentStore.slots.length"
              class="state-msg"
            >
              No available slots.
            </div>

            <template v-else>

              <div
                v-if="providerStore.providerProfile.provider.offers_home_service"
                class="location-section"
              >
                <div class="location-label">
                  Set your location
                </div>

                <div class="location-map">
                  <LocationPickerMap @location-selected="setLocation" />
                </div>

                <p v-if="customerLat && customerLng" class="coords-hint">
                  {{ customerLat.toFixed(4) }},
                  {{ customerLng.toFixed(4) }}
                </p>
              </div>

              <div class="slots">
                <div
                  v-for="slot in appointmentStore.slots"
                  :key="slot"
                  class="slot"
                >
                  <span class="slot-time">
                    {{ formatSlot(slot) }}
                  </span>

                  <button
                    class="confirm-btn"
                    :disabled="bookingLoading"
                    @click="book(service.id, slot)"
                  >
                    {{ bookingLoading ? "Booking..." : "Confirm" }}
                  </button>
                </div>
              </div>

            </template>

          </template>

        </div>
      </div>

    </template>
  </div>
</template>

<style scoped src="../../styles/customer/ProviderProfileView.css"></style>