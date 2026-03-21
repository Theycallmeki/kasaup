<script setup lang="ts">
import { computed, onMounted } from "vue"
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
</script>

<template>

<div>

<h2>Booking history</h2>

<p class="hint">
  All bookings, including cancelled. Active bookings also appear under
  <router-link to="/appointments">My appointments</router-link>.
</p>

<div v-if="appointmentStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="appointment in sortedAppointments"
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
.hint {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 16px;
}
</style>
