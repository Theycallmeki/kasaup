<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { useAppointmentStore } from "../../stores/appointmentStore"
import { useAuthStore } from "../../stores/authStore"
import { useScroll } from "../../hooks/useScroll"
import { useLoading } from "../../hooks/useLoading"
import CustomerLocationMapCard from "../../components/CustomerLocationMapCard.vue"

const appointmentStore = useAppointmentStore()
const authStore = useAuthStore()
const router = useRouter()
const { startLoading, stopLoading } = useLoading()
const { scrollRef: appointmentsScroll } = useScroll()
const activeTab = ref<"pending" | "upcoming" | "past">("pending")
const selectedApp = ref<any>(null)

onMounted(async () => {
  startLoading("Loading your schedule...")
  try {
    await appointmentStore.fetchAppointments()
  } finally {
    stopLoading()
  }
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
  selectedApp.value = selectedApp.value?.id === app.id ? null : app
}

watch(activeTab, () => {
  selectedApp.value = null
})

const approve = async (id: number) => {
  startLoading("Approving appointment...")
  try {
    await appointmentStore.approve(id)
  } finally {
    stopLoading()
  }
}

const cancel = async (id: number) => {
  startLoading("Canceling appointment...")
  try {
    await appointmentStore.cancel(id)
  } finally {
    stopLoading()
  }
}

const complete = async (id: number) => {
  startLoading("Completing appointment...")
  try {
    await appointmentStore.complete(id)
  } finally {
    stopLoading()
  }
}

function goToChat(app: any) {
  router.push({
    path: "/messages",
    query: {
      receiver_id: app.user_id,
      customer_name: app.customer_name
    }
  })
}

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
       <h1 class="title">Appointments</h1>
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

        <div v-else class="cards-grid" ref="appointmentsScroll">
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
                  <span v-if="app.customer_latitude && app.customer_longitude || app.customer_address" class="badge badge-home">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="display:inline;vertical-align:middle;margin-right:4px">
                      <polygon points="3 11 22 2 13 21 11 13 3 11"/>
                    </svg>
                    Home Service
                  </span>
                </div>
              </div>

              <div class="cust-info">
                 <div class="ci-avatar">
                   <img v-if="app.customer_profile_image" :src="app.customer_profile_image" alt="" class="ci-avatar-img" />
                   <span v-else>{{ app.customer_name.charAt(0).toUpperCase() }}</span>
                 </div>
                 <div class="ci-details">
                    <div class="ci-name">{{ app.customer_name }}</div>
                    <div v-if="app.customer_address" class="ci-address">
                      {{ app.customer_address }}
                    </div>
                 </div>
              </div>

              <!-- Actions row -->
              <div class="cb-bottom">
                <div class="cb-actions">
                  <button v-if="app.status === 'pending'" class="abtn abtn-green" @click="approve(app.id)">Approve</button>
                  <button v-if="app.status === 'approved' || app.status === 'confirmed'" class="abtn abtn-blue" @click="complete(app.id)">Complete</button>
                  <button class="abtn abtn-purple" @click="goToChat(app)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px;vertical-align:text-bottom">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    Message
                  </button>
                  <button v-if="app.status === 'pending' || app.status === 'approved' || app.status === 'confirmed'" class="abtn abtn-red" @click="cancel(app.id)">Cancel</button>
                </div>
                
                <button 
                  v-if="app.customer_latitude && app.customer_longitude || app.customer_address"
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
        :show="Boolean(selectedApp)"
        :lat="selectedApp?.customer_latitude ?? null"
        :lng="selectedApp?.customer_longitude ?? null"
        :customerName="selectedApp?.customer_name"
        :address="selectedApp?.customer_address"
        :providerLat="authStore.user?.latitude"
        :providerLng="authStore.user?.longitude"
      />
    </div>
  </div>
</template>

<style src="../../styles/provider/ProviderAppointmentsView.css" scoped></style>
