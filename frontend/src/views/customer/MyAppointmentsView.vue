<script setup lang="ts">
import { onMounted } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"

const appointmentStore = useAppointmentStore()

onMounted(() => {
  appointmentStore.fetchAppointments()
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
      >
        {{ appointment.appointment_time }}
      </div>

    </div>

  </div>
</template>