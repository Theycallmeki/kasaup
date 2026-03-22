<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(async () => {
  await appointmentStore.fetchAppointments()
})

const activeAppointments = computed(() => {
  return appointmentStore.appointments
    .filter((a) => a.status !== "cancelled")
    .sort(
      (a, b) =>
        new Date(a.appointment_time).getTime() -
        new Date(b.appointment_time).getTime()
    )
})

const cancel = async (id: number) => {
  await appointmentStore.cancel(id)
}

const statusClass = (status: string) => {
  if (status === "pending") return "badge-pending"
  if (status === "confirmed") return "badge-confirmed"
  if (status === "approved") return "badge-approved"
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
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">My Appointments</h1>
      <p class="subnav">
        View
        <router-link to="/appointments/history">booking history</router-link>
        for all statuses including cancelled
      </p>
    </div>

    <div v-if="appointmentStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
      Loading appointments...
    </div>

    <div v-else-if="activeAppointments.length === 0" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
      </svg>
      <p>No active appointments.</p>
      <p class="state-sub">Cancelled bookings are in <router-link to="/appointments/history">booking history</router-link>.</p>
    </div>

    <div v-else class="cards">
      <div
        v-for="appointment in activeAppointments"
        :key="appointment.id"
        class="card"
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

        <div class="card-divider" />

        <button
          v-if="canCancel(appointment.status)"
          class="cancel-btn"
          @click="cancel(appointment.id)"
        >
          Cancel Appointment
        </button>
      </div>
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

.subnav {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}
.subnav a {
  color: rgba(167, 139, 250, 0.8);
  text-decoration: none;
}
.subnav a:hover {
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
.state-sub {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.2);
}
.state-sub a {
  color: rgba(167, 139, 250, 0.7);
  text-decoration: none;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
.spin {
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px 20px;
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
.badge-pending  { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 0.5px solid rgba(251,191,36,0.3); }
.badge-confirmed { background: rgba(52,211,153,0.15); color: #34d399; border: 0.5px solid rgba(52,211,153,0.3); }
.badge-approved  { background: rgba(96,165,250,0.15); color: #60a5fa; border: 0.5px solid rgba(96,165,250,0.3); }
.badge-default   { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); border: 0.5px solid rgba(255,255,255,0.12); }

.card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 16px;
}

.card-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin-bottom: 16px;
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