<script setup lang="ts">
import { computed, onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(async () => {
  await appointmentStore.fetchAppointments()
})

/** Upcoming / active bookings only — cancelled are listed under booking history. */
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
</script>

<template>

<div>

<h2>My appointments</h2>

<p class="subnav">
  <router-link to="/appointments/history">Booking history</router-link>
  (all statuses, including cancelled)
</p>

<div v-if="appointmentStore.loading">
Loading...
</div>

<div v-else-if="activeAppointments.length === 0">
<p>No active appointments. Cancelled bookings are in
<router-link to="/appointments/history">booking history</router-link>.</p>
</div>

<div v-else>

<div
v-for="appointment in activeAppointments"
:key="appointment.id"
style="margin-bottom:14px; border:1px solid #ddd; padding:10px; border-radius:8px"
>

<div>
<strong>Service ID:</strong>
{{ appointment.service_id }}
</div>

<div>
<strong>Provider ID:</strong>
{{ appointment.provider_id }}
</div>

<div>
<strong>Time:</strong>
{{ appointment.appointment_time }}
</div>

<div>
<strong>Status:</strong>
{{ appointment.status }}
</div>

<div style="margin-top:8px">

<button
v-if="appointment.status === 'pending' || appointment.status === 'approved' || appointment.status === 'confirmed'"
@click="cancel(appointment.id)"
>
Cancel
</button>

</div>

</div>

</div>

</div>

</template>

<style scoped>
.subnav {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
}
</style>