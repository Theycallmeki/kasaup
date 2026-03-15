<script setup lang="ts">
import { onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(async () => {

  await appointmentStore.fetchAppointments()

})
</script>

<template>

<div>

<h2>Provider Appointments</h2>

<div v-if="appointmentStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="appointment in appointmentStore.appointments"
:key="appointment.id"
style="margin-bottom:12px"
>

<div>
<strong>Appointment Time:</strong>
{{ appointment.appointment_time }}
</div>

<div>
<strong>Service ID:</strong>
{{ appointment.service_id }}
</div>

<div>
<strong>Customer ID:</strong>
{{ appointment.user_id }}
</div>

<div>
<strong>Status:</strong>
{{ appointment.status }}
</div>

</div>

</div>

</div>

</template>