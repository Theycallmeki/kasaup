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

<h2>My Appointments</h2>

<div v-if="appointmentStore.loading">
Loading...
</div>

<div v-else>

<div
v-for="appointment in appointmentStore.appointments"
:key="appointment.id"
style="margin-bottom:14px"
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

</div>

</div>

</div>

</template>