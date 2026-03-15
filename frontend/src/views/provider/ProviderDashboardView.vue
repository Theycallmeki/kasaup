<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

function goServices() {
  router.push("/provider/services")
}

function goAppointments() {
  router.push("/provider/appointments")
}

function goAvailability() {
  router.push("/provider/availability")
}
</script>

<template>

<div class="dashboard">

  <h1>Provider Dashboard</h1>
  <p>Manage your services and appointments.</p>

  <div class="cards">

    <div class="card">
      <h3>My Services</h3>
      <p>Manage services you offer</p>
      <button @click="goServices">Manage Services</button>
    </div>

    <div class="card">
      <h3>Appointments</h3>
      <p>View upcoming bookings</p>
      <button @click="goAppointments">View Appointments</button>
    </div>

    <div class="card">
      <h3>Availability</h3>
      <p>Set your working schedule</p>
      <button @click="goAvailability">Manage Availability</button>
    </div>

  </div>

</div>

</template>

<style scoped>

.dashboard{
  padding:20px;
}

.cards{
  display:flex;
  gap:20px;
  margin-top:20px;
}

.card{
  background:white;
  padding:20px;
  border-radius:8px;
  box-shadow:0 5px 15px rgba(0,0,0,0.08);
  width:220px;
}

button{
  margin-top:10px;
  padding:8px 12px;
  border:none;
  background:#2563eb;
  color:white;
  border-radius:6px;
  cursor:pointer;
}

</style>