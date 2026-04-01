<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

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
              <div class="service-name">Service #{{ appointment.service_id }}</div>
              <div class="provider-label">Provider · #{{ appointment.provider_id }}</div>
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
        </div>
      </div>

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