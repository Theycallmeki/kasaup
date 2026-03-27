<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

function goServices()     { router.push("/provider/services") }
function goAppointments() { router.push("/provider/appointments") }
function goAvailability() { router.push("/provider/availability") }
function goProfile()      { router.push("/provider/profile") }
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">Provider Dashboard</h1>
      <p class="subtitle">Manage your services and appointments.</p>
    </div>

    <div class="cards">

      <div class="card">
        <div class="card-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
          </svg>
        </div>
        <h3 class="card-title">My Services</h3>
        <p class="card-desc">Manage the services you offer to customers.</p>
        <button class="card-btn" @click="goServices">
          Manage Services
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </div>

      <div class="card">
        <div class="card-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <line x1="16" y1="2" x2="16" y2="6"/>
            <line x1="8" y1="2" x2="8" y2="6"/>
            <line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
        </div>
        <h3 class="card-title">Appointments</h3>
        <p class="card-desc">View and manage your upcoming bookings.</p>
        <button class="card-btn" @click="goAppointments">
          View Appointments
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </div>

      <div class="card">
        <div class="card-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <h3 class="card-title">Availability</h3>
        <p class="card-desc">Set your working hours and schedule.</p>
        <button class="card-btn" @click="goAvailability">
          Manage Availability
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </div>

      <div class="card">
        <div class="card-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <h3 class="card-title">My Profile</h3>
        <p class="card-desc">View how customers see your provider profile.</p>
        <button class="card-btn" @click="goProfile">
          View Profile
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
}

.page-header {
  margin-bottom: 32px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.35);
  margin: 0;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  max-width: 780px;
}

.card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 24px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: border-color 0.2s;
}
.card:hover {
  border-color: rgba(167, 139, 250, 0.25);
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(99, 60, 220, 0.2);
  border: 0.5px solid rgba(130, 90, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a78bfa;
  margin-bottom: 4px;
}

.card-title {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin: 0;
}

.card-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.35);
  line-height: 1.5;
  flex: 1;
}

.card-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 9px 14px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  margin-top: 4px;
}
.card-btn:hover {
  background: rgba(99, 60, 220, 0.2);
  border-color: rgba(130, 90, 255, 0.3);
  color: #c4b5fd;
}

@media (max-width: 540px) {
  .page { padding: 24px 16px; }
  .cards { grid-template-columns: 1fr; }
}
</style>