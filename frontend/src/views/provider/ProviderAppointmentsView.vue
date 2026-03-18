<script setup lang="ts">
import { onMounted, nextTick } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"
import L from "leaflet"

const appointmentStore = useAppointmentStore()

onMounted(async () => {
  await appointmentStore.fetchAppointments()

  await nextTick()

  appointmentStore.appointments.forEach((appointment) => {
    if (
      appointment.customer_latitude &&
      appointment.customer_longitude
    ) {
      const mapId = `map-${appointment.id}`

      const map = L.map(mapId).setView(
        [
          appointment.customer_latitude,
          appointment.customer_longitude
        ],
        15
      )

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
      }).addTo(map)

      L.marker([
        appointment.customer_latitude,
        appointment.customer_longitude
      ]).addTo(map)
    }
  })
})

const confirm = async (id: number) => {
  await appointmentStore.confirm(id)
}

const cancel = async (id: number) => {
  await appointmentStore.cancel(id)
}

const complete = async (id: number) => {
  await appointmentStore.complete(id)
}
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

<div
v-if="appointment.customer_latitude && appointment.customer_longitude"
class="map-container"
>
<div :id="`map-${appointment.id}`" class="map"></div>
</div>

<div style="margin-top:10px; display:flex; gap:8px">

<button
v-if="appointment.status === 'pending'"
@click="confirm(appointment.id)"
>
Accept
</button>

<button
v-if="appointment.status === 'pending' || appointment.status === 'confirmed'"
@click="cancel(appointment.id)"
>
Cancel
</button>

<button
v-if="appointment.status === 'confirmed'"
@click="complete(appointment.id)"
>
Complete
</button>

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

.map-container{
margin-top:12px;
}

.map{
height:200px;
width:100%;
border-radius:8px;
}

</style>