<script setup lang="ts">
import { onMounted, nextTick } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"
import L from "leaflet"

const appointmentStore = useAppointmentStore()

onMounted(async () => {
  await appointmentStore.fetchAppointments()
  await nextTick()

  appointmentStore.appointments.forEach((appointment) => {
    if (appointment.customer_latitude && appointment.customer_longitude) {
      const mapId = `map-${appointment.id}`

      const map = L.map(mapId).setView(
        [appointment.customer_latitude, appointment.customer_longitude],
        15
      )

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(map)

      const customerIcon = L.divIcon({
        className: "",
        html: `<div class="kasaup-provider-pin"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
      })

      L.marker(
        [appointment.customer_latitude, appointment.customer_longitude],
        { icon: customerIcon }
      ).addTo(map)
    }
  })
})

const approve  = async (id: number) => { await appointmentStore.approve(id) }
const cancel   = async (id: number) => { await appointmentStore.cancel(id) }
const complete = async (id: number) => { await appointmentStore.complete(id) }

const statusClass = (status: string) => {
  if (status === "pending")   return "badge-pending"
  if (status === "confirmed") return "badge-confirmed"
  if (status === "approved")  return "badge-approved"
  if (status === "cancelled") return "badge-cancelled"
  if (status === "completed") return "badge-completed"
  return "badge-default"
}

const formatTime = (iso: string) =>
  new Date(iso).toLocaleString("en-PH", {
    month: "long", day: "numeric", year: "numeric",
    hour: "numeric", minute: "2-digit"
  })
</script>

<template>
  <div class="page">
    <h1 class="title">Provider Appointments</h1>

    <div v-if="appointmentStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
      </svg>
      Loading appointments...
    </div>

    <div v-else-if="appointmentStore.appointments.length === 0" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <rect x="3" y="4" width="18" height="18" rx="2"/>
        <line x1="16" y1="2" x2="16" y2="6"/>
        <line x1="8" y1="2" x2="8" y2="6"/>
        <line x1="3" y1="10" x2="21" y2="10"/>
      </svg>
      <p>No appointments yet.</p>
    </div>

    <div v-else class="cards">
      <div
        v-for="appointment in appointmentStore.appointments"
        :key="appointment.id"
        class="card"
      >
        <div class="card-top">
          <div>
            <div class="service-name">{{ appointment.service_name }}</div>
            <div class="customer-label">{{ appointment.customer_name }}</div>
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

        <div
          v-if="appointment.customer_latitude && appointment.customer_longitude"
          class="map-wrap"
        >
          <div class="map-label">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            Customer Location
          </div>
          <div :id="`map-${appointment.id}`" class="map" />
        </div>

        <div class="card-actions">
          <button
            v-if="appointment.status === 'pending'"
            class="action-btn btn-approve"
            @click="approve(appointment.id)"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            Approve
          </button>

          <button
            v-if="appointment.status === 'approved' || appointment.status === 'confirmed'"
            class="action-btn btn-complete"
            @click="complete(appointment.id)"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            Complete
          </button>

          <button
            v-if="appointment.status === 'pending' || appointment.status === 'approved' || appointment.status === 'confirmed'"
            class="action-btn btn-cancel"
            @click="cancel(appointment.id)"
          >
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancel
          </button>
        </div>
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

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 28px;
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
  gap: 6px;
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; margin-bottom: 8px; }

.cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 680px;
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
  margin-bottom: 12px;
}

.service-name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 3px;
}

.customer-label {
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
.badge-completed { background: rgba(167,139,250,0.15); color: #a78bfa; border: 0.5px solid rgba(167,139,250,0.3); }
.badge-default   { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); border: 0.5px solid rgba(255,255,255,0.12); }

.card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 16px;
}

.map-wrap {
  margin-bottom: 16px;
  border-radius: 10px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.07);
}

.map-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.25);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.06);
}

.map {
  height: 180px;
  width: 100%;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.15s;
}
.action-btn:hover { opacity: 0.8; }

.btn-approve {
  background: rgba(52, 211, 153, 0.12);
  border: 0.5px solid rgba(52, 211, 153, 0.3);
  color: #34d399;
}
.btn-complete {
  background: rgba(167, 139, 250, 0.12);
  border: 0.5px solid rgba(167, 139, 250, 0.3);
  color: #a78bfa;
}
.btn-cancel {
  background: rgba(248, 113, 113, 0.08);
  border: 0.5px solid rgba(248, 113, 113, 0.25);
  color: rgba(248, 113, 113, 0.8);
}

@media (max-width: 540px) {
  .page { padding: 24px 16px; }
}
</style>

<style>
.kasaup-provider-pin {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #a78bfa;
  box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.25);
}
</style>