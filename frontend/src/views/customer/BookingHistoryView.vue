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
  if (status === "pending")   return "badge-pending"
  if (status === "confirmed") return "badge-confirmed"
  if (status === "approved")  return "badge-approved"
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
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
      </svg>
      <p>No bookings yet.</p>
    </div>

    <div v-else class="cards">
      <p v-if="sortedAppointments.length" class="range-hint">
        Showing {{ rangeStart }}–{{ rangeEnd }} of {{ sortedAppointments.length }}
      </p>
      <div class="cards-scroll">
        <div
          v-for="appointment in paginatedAppointments"
          :key="appointment.id"
          class="card"
          :class="{ 'card-cancelled': appointment.status === 'cancelled' }"
        >
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
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/>
              <line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
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

      <nav v-if="totalPages > 1" class="pagination" aria-label="Booking history pages">
        <button
          type="button"
          class="page-nav-btn"
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
        >
          Previous
        </button>
        <div class="page-numbers">
          <template v-for="(p, idx) in pageNumbers" :key="`p-${idx}-${p}`">
            <span v-if="p === '...'" class="page-ellipsis" aria-hidden="true">…</span>
            <button
              v-else
              type="button"
              class="page-num"
              :class="{ active: p === currentPage }"
              @click="goToPage(p as number)"
            >
              {{ p }}
            </button>
          </template>
        </div>
        <button
          type="button"
          class="page-nav-btn"
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Next
        </button>
      </nav>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
}

.page-header {
  margin-bottom: 28px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}
.hint a {
  color: rgba(167, 139, 250, 0.8);
  text-decoration: none;
}
.hint a:hover {
  color: #a78bfa;
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
  gap: 6px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
.spin {
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

.range-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  margin: 0 0 14px;
}

.cards {
  display: flex;
  flex-direction: column;
}

.pagination {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px 16px;
  margin-top: 20px;
  padding-top: 8px;
}

.page-nav-btn {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  transition: background 0.15s, opacity 0.15s;
}
.page-nav-btn:hover:not(:disabled) {
  background: rgba(167, 139, 250, 0.12);
  border-color: rgba(167, 139, 250, 0.25);
}
.page-nav-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.page-num {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  min-width: 36px;
  height: 36px;
  padding: 0 8px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.65);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}
.page-num:hover {
  background: rgba(167, 139, 250, 0.1);
  border-color: rgba(167, 139, 250, 0.2);
  color: #fff;
}
.page-num.active {
  background: rgba(124, 58, 237, 0.35);
  border-color: rgba(167, 139, 250, 0.45);
  color: #fff;
}

.page-ellipsis {
  color: rgba(255, 255, 255, 0.25);
  font-size: 13px;
  padding: 0 4px;
  user-select: none;
}

.cards-scroll {
  max-height: 70vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 6px;
  scrollbar-width: thin;
  scrollbar-color: #a78bfa rgba(255,255,255,0.05);
}

.cards-scroll::-webkit-scrollbar {
  width: 8px;
}

.cards-scroll::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
}

.cards-scroll::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #a78bfa, #7c3aed);
  border-radius: 10px;
}

.cards-scroll::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #c4b5fd, #8b5cf6);
}

.card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px 20px;
  transition: opacity 0.2s;
}

.card-cancelled {
  opacity: 0.5;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}

.service-name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 3px;
}

.provider-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
}

.badge {
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 100px;
  letter-spacing: 0.04em;
  text-transform: capitalize;
  flex-shrink: 0;
}
.badge-pending   { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 0.5px solid rgba(251,191,36,0.3); }
.badge-confirmed { background: rgba(52,211,153,0.15);  color: #34d399; border: 0.5px solid rgba(52,211,153,0.3); }
.badge-approved  { background: rgba(96,165,250,0.15);  color: #60a5fa; border: 0.5px solid rgba(96,165,250,0.3); }
.badge-cancelled { background: rgba(248,113,113,0.1);  color: rgba(248,113,113,0.6); border: 0.5px solid rgba(248,113,113,0.2); }
.badge-default   { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); border: 0.5px solid rgba(255,255,255,0.12); }

.card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
}

.card-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin: 16px 0;
}

.cancel-btn {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(248, 113, 113, 0.08);
  border: 0.5px solid rgba(248, 113, 113, 0.25);
  color: rgba(248, 113, 113, 0.8);
  cursor: pointer;
  transition: opacity 0.15s;
}
.cancel-btn:hover {
  opacity: 0.8;
}

@media (max-width: 640px) {
  .page {
    padding: 24px 16px;
  }
}
</style>