<script setup lang="ts">
import { onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(async () => {
  await appointmentStore.fetchAppointments()
})

const cancel = async (id: number) => {
  await appointmentStore.cancel(id)
}
</script>

<template>

<div>

<h2>My Appointments</h2>

<div v-if="appointmentStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="appointment in appointmentStore.appointments"
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
v-if="appointment.status === 'pending' || appointment.status === 'confirmed'"
@click="cancel(appointment.id)"
>
Cancel
</button>

</div>

</div>

</div>

</div>

</template>