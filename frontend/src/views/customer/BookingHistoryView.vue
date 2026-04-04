<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"
import RatingModal from "../../components/RatingModal.vue"

const appointmentStore = useAppointmentStore()

const ratingModalOpen = ref(false)
const selectedAppointmentId = ref<number | null>(null)

const openRatingModal = (id: number) => {
  selectedAppointmentId.value = id
  ratingModalOpen.value = true
}

const onRatingSuccess = () => {
  // Optionally refresh appointments to reflect rating status
  appointmentStore.fetchAppointments()
}

onMounted(async () => {
  await appointmentStore.fetchAppointments()
})

const sortedAppointments = computed(() => {
  return [...appointmentStore.appointments].sort(
    (a, b) =>
      new Date(b.appointment_time).getTime() -
      new Date(a.appointment_time).getTime()
  )
})

const cancel = async (id: number) => {
  await appointmentStore.cancel(id)
}

const statusClass = (status: string) => {
  if (status === "pending") return "badge-pending"
  if (status === "confirmed") return "badge-confirmed"
  if (status === "approved") return "badge-approved"
  if (status === "cancelled") return "badge-cancelled"
  return "badge-default"
}

const formatTime = (iso: string) => {
  return new Date(iso).toLocaleString("en-PH", {
    month: "long",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit"
  })
}

const canCancel = (status: string) =>
  ["pending", "approved", "confirmed"].includes(status)

const PAGE_SIZE = 10
const currentPage = ref(1)

const totalPages = computed(() =>
  Math.ceil(sortedAppointments.value.length / PAGE_SIZE)
)

const paginatedAppointments = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return sortedAppointments.value.slice(start, start + PAGE_SIZE)
})

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

const pageNumbers = computed(() => {
  const pages: (number | string)[] = []
  const total = totalPages.value
  const cur = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (cur > 3) pages.push("...")
    for (let i = Math.max(2, cur - 1); i <= Math.min(total - 1, cur + 1); i++) pages.push(i)
    if (cur < total - 2) pages.push("...")
    pages.push(total)
  }
  return pages
})

const rangeStart = computed(() =>
  sortedAppointments.value.length === 0
    ? 0
    : (currentPage.value - 1) * PAGE_SIZE + 1
)

const rangeEnd = computed(() =>
  Math.min(currentPage.value * PAGE_SIZE, sortedAppointments.value.length)
)

watch(totalPages, (tp) => {
  if (tp > 0 && currentPage.value > tp) currentPage.value = tp
})
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">Booking History</h1>
      <p class="hint">
        All bookings including cancelled. Active bookings also appear under
        <router-link to="/appointments">My Appointments</router-link>.
      </p>
    </div>

    <div v-if="appointmentStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
      Loading history...
    </div>

    <div v-else-if="sortedAppointments.length === 0" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
        style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
      </svg>
      <p>No bookings yet.</p>
    </div>

    <div v-else class="cards">
      <p v-if="sortedAppointments.length" class="range-hint">
        Showing {{ rangeStart }}–{{ rangeEnd }} of {{ sortedAppointments.length }}
      </p>

      <div class="cards-scroll">
        <div v-for="appointment in paginatedAppointments" :key="appointment.id" class="card"
          :class="{ 'card-cancelled': appointment.status === 'cancelled' }">
          <div class="card-top">
            <div>
              <div class="service-name">{{ appointment.service_name }}</div>
              <div class="provider-label">Provider • {{ appointment.provider_name }}</div>
            </div>
            <span class="badge" :class="statusClass(appointment.status)">
              {{ appointment.status }}
            </span>
          </div>

          <div class="card-meta">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            {{ formatTime(appointment.appointment_time) }}
          </div>

          <div v-if="canCancel(appointment.status)">
            <div class="card-divider" />
            <button class="cancel-btn" @click="cancel(appointment.id)">
              Cancel Appointment
            </button>
          </div>

          <div v-if="appointment.status === 'completed'">
            <div class="card-divider" />
            <div v-if="appointment.user_rating" class="rated-stars">
              <span class="rated-label">Your Rating:</span>
              <div class="stars-display">
                <svg v-for="i in 5" :key="i" width="14" height="14" viewBox="0 0 24 24" 
                     :fill="i <= appointment.user_rating ? '#fbbf24' : 'none'" 
                     :stroke="i <= appointment.user_rating ? '#fbbf24' : 'currentColor'" 
                     stroke-width="2">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
            </div>
            <button v-else class="rate-btn" @click="openRatingModal(appointment.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" style="margin-right:6px">
                <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
              </svg>
              Rate Service
            </button>
          </div>
        </div>
      </div>

      <RatingModal 
        :is-open="ratingModalOpen" 
        :appointment-id="selectedAppointmentId || 0"
        @close="ratingModalOpen = false"
        @success="onRatingSuccess"
      />

      <nav v-if="totalPages > 1" class="pagination">
        <button class="page-nav-btn" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">
          Previous
        </button>

        <div class="page-numbers">
          <template v-for="(p, idx) in pageNumbers" :key="idx">
            <span v-if="p === '...'" class="page-ellipsis">…</span>
            <button v-else class="page-num" :class="{ active: p === currentPage }" @click="goToPage(p as number)">
              {{ p }}
            </button>
          </template>
        </div>

        <button class="page-nav-btn" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">
          Next
        </button>
      </nav>
    </div>

  </div>
</template>

<style scoped src="../../styles/customer/BookingHistoryView.css"></style>