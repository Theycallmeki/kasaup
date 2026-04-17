<script setup lang="ts">
import { onMounted, ref, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import { useAppointmentStore } from "../../stores/appointmentStore"
import HomeServiceMapCard from "../../components/HomeServiceMapCard.vue"
import api from "../../services/api"
import { useNotification } from "../../hooks/useNotification"
import { useLoading } from "../../hooks/useLoading"
 
const router = useRouter()
const { notifySuccess, notifyError } = useNotification()
const { startLoading, stopLoading } = useLoading()
const route = useRoute()
const providerStore = useProviderStore()
const appointmentStore = useAppointmentStore()

const id = Number(route.params.id)

const messageProvider = async () => {
    const provider = providerStore.providerProfile.provider;
    router.push({ 
        path: '/messages', 
        query: { 
            provider_id: provider.id,
            receiver_id: provider.owner_id,
            shop_name: provider.shop_name
        } 
    });
}

const activeServiceId = ref<number | null>(null)
const selectedDate = ref<string>("")
const serviceLocationType = ref<"shop" | "home">("shop")
const customerLat = ref<number | null>(null)
const customerLng = ref<number | null>(null)
const lightboxImg = ref<string | null>(null)

// Custom confirm dialog state
const confirmDialog = ref(false)
const pendingBooking = ref<{ serviceId: number; slot: string } | null>(null)

const imageIndices = ref<Record<number, number>>({})
function getImgIndex(serviceId: number) { return imageIndices.value[serviceId] || 0 }
function nextImg(serviceId: number, max: number) { imageIndices.value[serviceId] = (getImgIndex(serviceId) + 1) % max }
function prevImg(serviceId: number, max: number) { imageIndices.value[serviceId] = (getImgIndex(serviceId) - 1 + max) % max }
function setImg(serviceId: number, idx: number) { imageIndices.value[serviceId] = idx }

const loadingSlots = ref(false)
const bookingLoading = ref(false)
const errorMsg = ref("")

const calendarYear = ref(new Date().getFullYear())
const calendarMonth = ref(new Date().getMonth())

const availableDates = ref<Set<string>>(new Set())
const loadingAvailable = ref(false)

const imgUrl = (path: string) => {
  if (!path) return ""
  if (path.startsWith("http")) return path
  return `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}`
}

onMounted(async () => {
  startLoading("Syncing provider details...")
  try {
    await providerStore.fetchProviderProfile(id)
  } catch (e) {
    errorMsg.value = "Failed to load provider."
  } finally {
    stopLoading()
  }
})

async function loadSlots(serviceId: number) {
  activeServiceId.value = serviceId
  selectedDate.value = ""
  serviceLocationType.value = "shop"
  errorMsg.value = ""
  await loadAvailableDatesForMonth()
}

async function loadAvailableDatesForMonth() {
  if (!activeServiceId.value) return
  loadingAvailable.value = true
  availableDates.value = new Set()

  const year = calendarYear.value
  const month = calendarMonth.value
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const checks: Promise<void>[] = []

  for (let d = 1; d <= daysInMonth; d++) {
    const dateObj = new Date(year, month, d)
    if (dateObj < today) continue
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`
    checks.push(
      appointmentStore.fetchAvailableSlots(activeServiceId.value!, dateStr).then(() => {
        if (appointmentStore.slots.length > 0) {
          availableDates.value = new Set([...availableDates.value, dateStr])
        }
      }).catch(() => { })
    )
  }

  await Promise.all(checks)
  loadingAvailable.value = false
}

watch([calendarYear, calendarMonth], () => {
  if (activeServiceId.value) loadAvailableDatesForMonth()
})

async function fetchSlots() {
  if (!activeServiceId.value || !selectedDate.value) return
  startLoading("Retrieving available times...")
  loadingSlots.value = true
  try {
    await appointmentStore.fetchAvailableSlots(activeServiceId.value, selectedDate.value)
  } catch (e) {
    errorMsg.value = "Failed to load available slots."
  } finally {
    loadingSlots.value = false
    stopLoading()
  }
}

function setLocation(data: any) {
  customerLat.value = data.latitude
  customerLng.value = data.longitude
}

function book(serviceId: number, slot: string) {
  pendingBooking.value = { serviceId, slot }
  confirmDialog.value = true
}

function cancelBooking() {
  confirmDialog.value = false
  pendingBooking.value = null
}

function acceptBooking() {
  confirmDialog.value = false
  if (pendingBooking.value) {
    proceedWithBooking(pendingBooking.value.serviceId, pendingBooking.value.slot)
    pendingBooking.value = null
  }
}

async function proceedWithBooking(serviceId: number, slot: string) {
  startLoading("Securing your appointment...")
  bookingLoading.value = true
  errorMsg.value = ""
  try {
    const [dateStr, timeStrFull] = slot.split("T")
    const timeStr = timeStrFull.slice(0, 5)

    const isHome = serviceLocationType.value === "home"
    if (isHome && (!customerLat.value || !customerLng.value)) {
      const msg = "Please pin your location for Home Service."
      errorMsg.value = msg
      notifyError("Location Required", msg)
      bookingLoading.value = false
      return
    }

    await appointmentStore.bookAppointment({
      provider_id: id,
      service_id: serviceId,
      date: dateStr,
      time: timeStr,
      customer_latitude: isHome ? customerLat.value : null,
      customer_longitude: isHome ? customerLng.value : null
    })

    notifySuccess("Success", "Appointment booked successfully!")
    await fetchSlots()
    await appointmentStore.fetchAppointments()
  } catch (e: any) {
    const msg = e.response?.data?.detail || "Booking failed. Try again."
    errorMsg.value = msg
    notifyError("Booking Error", msg)
  } finally {
    bookingLoading.value = false
    stopLoading()
  }
}

const formatSlot = (iso: string) =>
  new Date(iso).toLocaleString("en-PH", {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true
  })

const formatTimeOnly = (iso: string) =>
  new Date(iso).toLocaleTimeString("en-PH", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true
  })

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
]
const DAY_LABELS = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

const calendarLabel = computed(() =>
  `${MONTH_NAMES[calendarMonth.value]} ${calendarYear.value}`
)

const calendarDays = computed(() => {
  const year = calendarYear.value
  const month = calendarMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const cells: ({ day: number; dateStr: string } | null)[] = []

  for (let i = 0; i < firstDay; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`
    cells.push({ day: d, dateStr })
  }
  return cells
})

const today = new Date()
today.setHours(0, 0, 0, 0)

function isPast(dateStr: string) {
  return new Date(dateStr) < today
}

function isAvailable(dateStr: string) {
  return availableDates.value.has(dateStr)
}

function isSelected(dateStr: string) {
  return selectedDate.value === dateStr
}

function isToday(dateStr: string) {
  const t = new Date()
  const ts = `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`
  return dateStr === ts
}

function selectDay(dateStr: string) {
  if (isPast(dateStr)) return
  selectedDate.value = dateStr
  fetchSlots()
}

function prevMonth() {
  if (calendarMonth.value === 0) {
    calendarMonth.value = 11
    calendarYear.value--
  } else {
    calendarMonth.value--
  }
}

function nextMonth() {
  if (calendarMonth.value === 11) {
    calendarMonth.value = 0
    calendarYear.value++
  } else {
    calendarMonth.value++
  }
}

const isPrevDisabled = computed(() => {
  const now = new Date()
  return calendarYear.value === now.getFullYear() && calendarMonth.value === now.getMonth()
})
</script>

<template>
  <div class="page">

    <div v-if="providerStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
      Loading provider...
    </div>

    <div v-else-if="errorMsg" class="state-msg">
      {{ errorMsg }}
    </div>

    <div v-else-if="!providerStore.providerProfile" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
        style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <circle cx="12" cy="8" r="4" />
        <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
      </svg>
      Provider not found.
    </div>

    <template v-else>
      <div class="provider-header">
        <div class="provider-avatar" :class="{ 'has-img': providerStore.providerProfile.provider.profile_image }">
          <img v-if="providerStore.providerProfile.provider.profile_image"
            :src="imgUrl(providerStore.providerProfile.provider.profile_image)" alt="Profile" class="avatar-img" />
          <span v-else>{{ providerStore.providerProfile.provider.shop_name?.charAt(0) }}</span>
        </div>
        <div>
          <h1 class="provider-name">
            {{ providerStore.providerProfile.provider.shop_name }}
          </h1>
          <div class="provider-stats">
            <div class="rating-display">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="#fbbf24">
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
              </svg>
              <span>{{ providerStore.providerProfile.provider.rating.toFixed(1) }}</span>
              <span class="review-count">({{ providerStore.providerProfile.provider.total_reviews }} reviews)</span>
            </div>
          </div>
          <p class="provider-desc">
            {{ providerStore.providerProfile.provider.description }}
          </p>
          <div class="header-actions">
            <div v-if="providerStore.providerProfile.provider.offers_home_service" class="home-badge">
              Offers Home Service
            </div>
            <button class="chat-btn" @click="messageProvider">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              Message
            </button>
          </div>
        </div>
      </div>

      <div class="divider" />

      <h2 class="section-title">Services</h2>

      <div class="profile-layout">
        <div class="profile-main">
          <div v-if="!providerStore.providerProfile.services.length" class="state-msg">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
              style="color:rgba(255,255,255,0.15);margin-bottom:12px">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" />
              <rect x="9" y="3" width="6" height="4" rx="1" />
            </svg>
            No services available.
          </div>

          <div v-else class="services">
            <div v-for="service in providerStore.providerProfile.services" :key="service.id" class="service-card"
              :class="{ 'service-active': activeServiceId === service.id }">

              <div v-if="service.images?.length" class="modal-carousel">
                <button v-if="service.images.length > 1" @click.stop="prevImg(service.id, service.images.length)"
                  class="carousel-btn prev">‹</button>
                <div class="modal-carousel-track">
                  <img :src="imgUrl(service.images[getImgIndex(service.id)].image_url)" class="modal-carousel-img"
                    @click="lightboxImg = imgUrl(service.images[getImgIndex(service.id)].image_url)" />
                </div>
                <button v-if="service.images.length > 1" @click.stop="nextImg(service.id, service.images.length)"
                  class="carousel-btn next">›</button>
                <div v-if="service.images.length > 1" class="carousel-dots">
                  <span v-for="(_, i) in service.images" :key="i" class="carousel-dot"
                    :class="{ active: Number(i) === getImgIndex(service.id) }"
                    @click.stop="setImg(service.id, Number(i))"></span>
                </div>
              </div>

              <div class="service-top">
                <div>
                  <div class="service-name">{{ service.name }}</div>
                  <div class="service-meta">
                    <span class="meta-pill">₱{{ service.price }}</span>
                    <span class="meta-pill">{{ service.duration_minutes }} min</span>
                  </div>
                </div>

                <button class="book-btn" :class="{ 'book-btn-active': activeServiceId === service.id }"
                  @click="loadSlots(service.id)">
                  {{ activeServiceId === service.id ? 'Viewing slots' : 'Book' }}
                </button>
              </div>

              <div v-if="activeServiceId === service.id" class="service-body">

                <div class="service-left">
                  <div v-if="loadingSlots" class="state-msg" style="padding: 24px 18px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                      class="spin">
                      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                    </svg>
                    Loading slots...
                  </div>

                  <div v-else-if="!selectedDate" class="state-msg" style="padding: 32px 18px;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
                      style="color:rgba(255,255,255,0.12);margin-bottom:8px">
                      <rect x="3" y="4" width="18" height="18" rx="2" />
                      <line x1="16" y1="2" x2="16" y2="6" />
                      <line x1="8" y1="2" x2="8" y2="6" />
                      <line x1="3" y1="10" x2="21" y2="10" />
                    </svg>
                    Pick a date to see slots.
                  </div>

                  <div v-else-if="selectedDate && !appointmentStore.slots.length" class="state-msg"
                    style="padding: 24px 18px;">
                    No available slots for this date.
                  </div>

                  <template v-else-if="selectedDate">
                    <div v-if="providerStore.providerProfile.provider.offers_home_service" class="location-section"
                      style="margin-bottom: 24px; border-top: none; padding-top: 0;">
                      <div class="location-label">Service Location</div>
                      <div class="location-toggle">
                        <button :class="{ active: serviceLocationType === 'shop' }"
                          @click="serviceLocationType = 'shop'">At Shop</button>
                        <button :class="{ active: serviceLocationType === 'home' }"
                          @click="serviceLocationType = 'home'">Home Service</button>
                      </div>
                    </div>

                    <div class="slots">
                      <div v-for="slot in appointmentStore.slots" :key="slot.start_time" class="slot">
                        <span class="slot-time">{{ formatSlot(slot.start_time) }} - {{ formatTimeOnly(slot.end_time)
                          }}</span>
                        <button class="confirm-btn" :disabled="bookingLoading"
                          @click="book(service.id, slot.start_time)">
                          {{ bookingLoading ? "Booking..." : "Confirm" }}
                        </button>
                      </div>
                    </div>
                  </template>
                </div>

                <div class="service-right">
                  <div class="calendar-section">
                    <div class="calendar-header">
                      <button class="cal-nav" :disabled="isPrevDisabled" @click="prevMonth">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2.5">
                          <polyline points="15 18 9 12 15 6" />
                        </svg>
                      </button>
                      <span class="cal-label">
                        {{ calendarLabel }}
                        <span v-if="loadingAvailable" class="cal-loading">
                          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="2" class="spin">
                            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                          </svg>
                        </span>
                      </span>
                      <button class="cal-nav" @click="nextMonth">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                          stroke-width="2.5">
                          <polyline points="9 18 15 12 9 6" />
                        </svg>
                      </button>
                    </div>

                    <div class="cal-grid">
                      <div v-for="label in DAY_LABELS" :key="label" class="cal-day-label">
                        {{ label }}
                      </div>

                      <template v-for="(cell, idx) in calendarDays" :key="idx">
                        <div v-if="cell === null" class="cal-cell cal-empty" />
                        <div v-else class="cal-cell" :class="{
                          'cal-past': isPast(cell.dateStr),
                          'cal-available': !isPast(cell.dateStr) && isAvailable(cell.dateStr),
                          'cal-selected': isSelected(cell.dateStr),
                          'cal-today': isToday(cell.dateStr) && !isSelected(cell.dateStr),
                        }" @click="selectDay(cell.dateStr)">
                          {{ cell.day }}
                          <span
                            v-if="!isPast(cell.dateStr) && isAvailable(cell.dateStr) && !isSelected(cell.dateStr)"
                            class="cal-dot" />
                        </div>
                      </template>
                    </div>

                    <div class="cal-legend">
                      <span class="legend-item">
                        <span class="legend-dot legend-dot-available" />
                        Available
                      </span>
                      <span class="legend-item">
                        <span class="legend-dot legend-dot-past" />
                        Unavailable
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <HomeServiceMapCard
                v-if="activeServiceId === service.id"
                :show="Boolean(selectedDate && serviceLocationType === 'home' && providerStore.providerProfile.provider.offers_home_service)"
                :customerLat="customerLat" :customerLng="customerLng" @location-selected="setLocation" />
            </div>
          </div>
        </div>

      </div>
    </template>

    <!-- Custom Confirm Dialog -->
    <Teleport to="body">
      <div v-if="confirmDialog" class="custom-dialog-overlay" @click.self="cancelBooking">
        <div class="custom-dialog">
          <div class="custom-dialog-header">
            <div class="custom-dialog-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <h3 class="custom-dialog-title">Confirm Booking</h3>
            <button class="custom-dialog-close" @click="cancelBooking">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <p class="custom-dialog-message">Are you sure you want to book this appointment?</p>
          <div class="custom-dialog-actions">
            <button class="custom-dialog-cancel" @click="cancelBooking">No, cancel</button>
            <button class="custom-dialog-confirm" @click="acceptBooking">Yes, book it</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Lightbox -->
    <Teleport to="body">
      <div v-if="lightboxImg" class="lightbox-overlay" @click="lightboxImg = null">
        <img :src="lightboxImg" class="lightbox-img" @click.stop />
        <button class="lightbox-close" @click="lightboxImg = null">✕</button>
      </div>
    </Teleport>

    <!-- Bottom Spacer for mobile scroller -->
    <div class="bottom-spacer" />

  </div>
</template>

<style scoped src="../../styles/customer/ProviderProfileView.css"></style>