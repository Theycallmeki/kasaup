<script setup lang="ts">
import { onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(async () => {

  await appointmentStore.fetchAppointments()

})
</script>

<template>

<div class="appointments">

<h2>Provider Appointments</h2>

<div v-if="appointmentStore.loading">
Loading appointments...
</div>

<div v-else>

<div
v-for="appointment in appointmentStore.appointments"
:key="appointment.id"
class="appointment-card"
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

<style scoped>

.appointments{
padding:20px;
}

.appointment-card{
background:white;
border-radius:8px;
padding:16px;
margin-bottom:12px;
box-shadow:0 5px 15px rgba(0,0,0,0.08);
}

</style>