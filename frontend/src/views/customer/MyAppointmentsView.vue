<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"
import { useLoading } from "../../hooks/useLoading"

const appointmentStore = useAppointmentStore()
const { startLoading, stopLoading } = useLoading()

onMounted(async () => {
  startLoading("Loading your appointments...")
  try {
    await appointmentStore.fetchAppointments()
  } finally {
    stopLoading()
  }
})

const activeAppointments = computed(() => {
  return appointmentStore.appointments
    .filter((a) => ["pending", "approved"].includes(a.status))
    .sort(
      (a, b) =>
        new Date(a.appointment_time).getTime() -
        new Date(b.appointment_time).getTime()
    )
})

const cancel = async (id: number) => {
  startLoading("Canceling appointment...")
  try {
    await appointmentStore.cancel(id)
  } finally {
    stopLoading()
  }
}

const statusClass = (status: string) => {
  if (status === "pending") return "badge-pending"
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
  ["pending", "approved"].includes(status)
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
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
        style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <rect x="3" y="4" width="18" height="18" rx="2" />
        <line x1="16" y1="2" x2="16" y2="6" />
        <line x1="8" y1="2" x2="8" y2="6" />
        <line x1="3" y1="10" x2="21" y2="10" />
      </svg>
      <p>No active appointments.</p>
      <p class="state-sub">
        Cancelled bookings are in
        <router-link to="/appointments/history">booking history</router-link>.
      </p>
    </div>

    <div v-else class="cards">
      <div v-for="appointment in activeAppointments" :key="appointment.id" class="card">
        <div class="card-top">
          <div>
            <div class="service-name">
              {{ appointment.service_name }}
            </div>
            <div class="provider-label">
              Provider • {{ appointment.provider_name }}
            </div>
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

        <div class="card-divider" />

        <button v-if="canCancel(appointment.status)" class="cancel-btn" @click="cancel(appointment.id)">
          Cancel Appointment
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped src="../../styles/customer/MyAppointmentsView.css"></style>