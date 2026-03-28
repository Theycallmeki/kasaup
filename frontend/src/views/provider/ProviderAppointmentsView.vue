<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { useAppointmentStore } from "../../stores/appointmentStore"
import CustomerLocationMapCard from "../../components/CustomerLocationMapCard.vue"

const appointmentStore = useAppointmentStore()
const activeTab = ref<"pending" | "upcoming" | "past">("pending")
const selectedApp = ref<any>(null)

onMounted(async () => {
  await appointmentStore.fetchAppointments()
})

const filteredItems = computed(() => {
  return appointmentStore.appointments.filter(a => {
    if (activeTab.value === 'pending') return a.status === 'pending'
    if (activeTab.value === 'upcoming') return a.status === 'approved' || a.status === 'confirmed'
    if (activeTab.value === 'past') return a.status === 'completed' || a.status === 'cancelled'
    return false
  }).sort((a,b) => new Date(a.appointment_time).getTime() - new Date(b.appointment_time).getTime())
})

function selectApp(app: any) {
  if (!app.customer_latitude || !app.customer_longitude) return
  selectedApp.value = selectedApp.value?.id === app.id ? null : app
}

watch(activeTab, () => {
  selectedApp.value = null
})

const approve  = async (id: number) => { await appointmentStore.approve(id) }
const cancel   = async (id: number) => { await appointmentStore.cancel(id) }
const complete = async (id: number) => { await appointmentStore.complete(id) }

const statusClass = (status: string) => {
  if (status === "pending")   return "badge-pending"
  if (status === "confirmed") return "badge-confirmed"
  if (status === "approved")  return "badge-approved"
  if (status === "cancelled") return "badge-cancelled"
  if (status === "completed") return "badge-completed"
  return "badge-default"
}

const formatDateTime = (iso: string) => {
  const d = new Date(iso)
  return {
    date: d.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    time: d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }),
    year: d.getFullYear()
  }
}
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
         <p class="eyebrow">Your Schedule</p>
         <h1 class="title">Appointments</h1>
      </div>
      <div class="stats-row">
         <div class="stat-pill">
           <span>Pending</span>
           <b>{{ appointmentStore.appointments.filter((a: any) => a.status==='pending').length }}</b>
         </div>
         <div class="stat-pill active-stat">
           <span>Upcoming</span>
           <b>{{ appointmentStore.appointments.filter((a: any) => a.status==='approved' || a.status==='confirmed').length }}</b>
         </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-container">
      <div class="tabs">
        <button class="tab-btn" :class="{active: activeTab==='pending'}" @click="activeTab='pending'">
          Pending Requests
        </button>
        <button class="tab-btn" :class="{active: activeTab==='upcoming'}" @click="activeTab='upcoming'">
          Upcoming
        </button>
        <button class="tab-btn" :class="{active: activeTab==='past'}" @click="activeTab='past'">
          Past / Cancelled
        </button>
      </div>
    </div>

    <div class="appointments-layout">
      <div class="appointments-main">
        <div v-if="appointmentStore.loading" class="state-msg">
          <span class="spin"></span> <p>Syncing schedule...</p>
        </div>

        <div v-else-if="filteredItems.length === 0" class="state-msg empty">
          <div class="empty-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M8 12l3 3 5-5"/>
            </svg>
          </div>
          <h3 class="empt-text">No {{ activeTab }} appointments!</h3>
          <p class="empt-sub">You have a clear schedule right now.</p>
        </div>

        <div v-else class="cards-grid">
          <div
            v-for="app in filteredItems"
            :key="app.id"
            class="app-card"
            :class="{ 'app-card-selected': selectedApp?.id === app.id }"
          >
            
            <!-- Left Strip for Timing -->
            <div class="card-left-strip">
              <div class="cd-date">{{ formatDateTime(app.appointment_time).date }}</div>
              <div class="cd-time">{{ formatDateTime(app.appointment_time).time }}</div>
            </div>

            <!-- Main Content Body -->
            <div class="card-body">
              <div class="cb-top">
                <h3 class="svc-name">{{ app.service_name }}</h3>
                <div class="cb-badges">
                  <span class="badge" :class="statusClass(app.status)">{{ app.status }}</span>
                  <span v-if="app.customer_latitude && app.customer_longitude" class="badge badge-home">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="display:inline;vertical-align:middle;margin-right:4px">
                      <polygon points="3 11 22 2 13 21 11 13 3 11"/>
                    </svg>
                    Home Service
                  </span>
                </div>
              </div>

              <div class="cust-info">
                 <div class="ci-avatar">{{ app.customer_name.charAt(0).toUpperCase() }}</div>
                 <div class="ci-name">{{ app.customer_name }}</div>
              </div>

              <!-- Actions row -->
              <div class="cb-bottom">
                <div class="cb-actions">
                  <button v-if="app.status === 'pending'" class="abtn abtn-green" @click="approve(app.id)">Approve</button>
                  <button v-if="app.status === 'approved' || app.status === 'confirmed'" class="abtn abtn-blue" @click="complete(app.id)">Complete</button>
                  <button v-if="app.status === 'pending' || app.status === 'approved' || app.status === 'confirmed'" class="abtn abtn-red" @click="cancel(app.id)">Cancel</button>
                </div>
                
                <button 
                  v-if="app.customer_latitude && app.customer_longitude"
                  class="map-toggle-btn"
                  :class="{ open: selectedApp?.id === app.id }"
                  @click="selectApp(app)"
                >
                  {{ selectedApp?.id === app.id ? 'Hide Map' : 'View Location' }}
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
                  </svg>
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

      <!-- Customer Location Map Card (right sidebar) -->
      <CustomerLocationMapCard
        :show="Boolean(selectedApp && selectedApp.customer_latitude && selectedApp.customer_longitude)"
        :lat="selectedApp?.customer_latitude ?? null"
        :lng="selectedApp?.customer_longitude ?? null"
        :customerName="selectedApp?.customer_name"
      />
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500;600;700&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
  color: #fff;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a78bfa;
  margin: 0 0 4px;
  font-weight: 600;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.02em;
}

.stats-row {
  display: flex;
  gap: 12px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.03);
  border: 0.5px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 10px 16px;
  min-width: 90px;
}
.stat-pill span {
  font-size: 10px;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}
.stat-pill b {
  font-family: 'Sora', sans-serif;
  font-size: 1.25rem;
  color: #fff;
  line-height: 1.2;
}
.active-stat {
  background: rgba(167, 139, 250, 0.1);
  border-color: rgba(167, 139, 250, 0.25);
}
.active-stat b { color: #c4b5fd; }

/* Tabs */
.tabs-container {
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding-bottom: 4px;
}
.tabs {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  scrollbar-width: none;
}
.tabs::-webkit-scrollbar { display: none; }
.tab-btn {
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.4);
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  padding: 8px 0;
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
  white-space: nowrap;
}
.tab-btn:hover { color: rgba(255,255,255,0.7); }
.tab-btn.active { color: #a78bfa; }
.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #a78bfa;
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
}

/* States */
.state-msg {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
  justify-content: center;
}
.state-msg.empty {
  flex-direction: column;
  background: rgba(255,255,255,0.015);
  border: 1px dashed rgba(255,255,255,0.1);
  border-radius: 20px;
}
.empty-icon {
  color: rgba(167,139,250,0.6);
  margin-bottom: 8px;
}
.empt-text {
  font-family: 'Sora', sans-serif;
  color: #fff;
  font-size: 1.25rem;
  margin: 0;
}
.empt-sub {
  margin: 4px 0 0;
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.1);
  border-top-color: #a78bfa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Grid layout */
.appointments-layout {
  display: flex;
  align-items: flex-start;
  gap: 32px;
}

.appointments-main {
  flex: 1;
  min-width: 0;
  max-width: 760px;
}

.cards-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Timeline Card */
.app-card {
  display: flex;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  transition: transform 0.2s, background 0.2s;
}
.app-card:hover {
  background: rgba(255, 255, 255, 0.035);
  border-color: rgba(255, 255, 255, 0.08);
}
.app-card-selected {
  border-color: rgba(56, 189, 248, 0.35) !important;
  background: rgba(56, 189, 248, 0.04) !important;
}

/* Left Strip */
.card-left-strip {
  width: 90px;
  background: rgba(255,255,255,0.02);
  border-right: 1px dashed rgba(255,255,255,0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 10px;
  flex-shrink: 0;
}
.cd-date {
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 1.1rem;
  color: #fff;
  text-align: center;
  line-height: 1.2;
}
.cd-time {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  font-weight: 500;
  margin-top: 4px;
}

/* Card Body */
.card-body {
  flex: 1;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
}

.cb-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.cb-badges {
  display: flex;
  gap: 6px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.svc-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
  margin-right: 12px;
}

.cust-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}

.ci-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(99,60,220,0.5), rgba(130,90,255,0.5));
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #fff;
}

.ci-name {
  font-size: 0.95rem;
  color: rgba(255,255,255,0.6);
  font-weight: 500;
}

.cb-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: auto;
}

.cb-actions {
  display: flex;
  gap: 8px;
}

.abtn {
  padding: 8px 16px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s, transform 0.1s;
}
.abtn:hover { opacity: 0.8; }
.abtn:active { transform: scale(0.97); }

.abtn-green {
  background: rgba(52, 211, 153, 0.15);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.2);
}
.abtn-blue {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.2);
}
.abtn-red {
  background: transparent;
  color: rgba(248, 113, 113, 0.6);
}
.abtn-red:hover {
  background: rgba(248, 113, 113, 0.1);
  color: #f87171;
}

.map-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  color: #a78bfa;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}
.map-toggle-btn.open {
  color: #38bdf8;
}

/* Map Dropdown */
.map-dropdown {
  overflow: hidden;
  max-height: 0;
  opacity: 0;
  transition: max-height 0.4s ease, opacity 0.4s ease, margin 0.4s ease;
}
.map-dropdown.show {
  max-height: 300px;
  opacity: 1;
  margin-top: 20px;
}
.map-container {
  height: 200px;
  width: 100%;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* Badges */
.badge {
  font-size: 10px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 100px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  flex-shrink: 0;
}
.badge-pending   { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 0.5px solid rgba(251,191,36,0.3); }
.badge-confirmed { background: rgba(52,211,153,0.15);  color: #34d399; border: 0.5px solid rgba(52,211,153,0.3); }
.badge-approved  { background: rgba(96,165,250,0.15);  color: #60a5fa; border: 0.5px solid rgba(96,165,250,0.3); }
.badge-cancelled { background: rgba(248,113,113,0.1);  color: rgba(248,113,113,0.6); border: 0.5px solid rgba(248,113,113,0.2); }
.badge-completed { background: rgba(167,139,250,0.15); color: #a78bfa; border: 0.5px solid rgba(167,139,250,0.3); }
.badge-default   { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.5); border: 0.5px solid rgba(255,255,255,0.12); }
.badge-home      { background: rgba(56,189,248,0.15); color: #38bdf8; border: 0.5px solid rgba(56,189,248,0.3); }

@media (max-width: 600px) {
  .page { padding: 20px 14px; }
  .app-card { flex-direction: column; }
  .card-left-strip {
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    padding: 12px 20px;
    border-right: none;
    border-bottom: 1px dashed rgba(255,255,255,0.05);
  }
}

@media (max-width: 900px) {
  .appointments-layout {
    flex-direction: column;
  }
  .appointments-main {
    max-width: 100%;
  }
}
</style>

<style>
.kasaup-provider-pin {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #38bdf8;
  box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.25);
}
</style>