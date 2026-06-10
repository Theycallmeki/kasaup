<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getOverview, getRecentActivity, getPendingUsers } from "../../services/admin"

const router = useRouter()

const overview = ref<any>(null)
const recentActivity = ref<any>(null)
const pendingUsers = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [overviewData, activityData, pendingData] = await Promise.all([
      getOverview(),
      getRecentActivity(),
      getPendingUsers()
    ])
    overview.value = overviewData
    recentActivity.value = activityData
    pendingUsers.value = pendingData
  } catch (e) {
    console.error("Failed to load admin dashboard data", e)
  } finally {
    loading.value = false
  }
})

function goUsers() {
  router.push("/admin/users")
}

function goProviders() {
  router.push("/admin/providers")
}

function goCategories() {
  router.push("/admin/categories")
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP' }).format(value)
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <div class="header-label">Admin</div>
      <h1 class="title">Dashboard</h1>
      <p class="hint">Overview of platform metrics and recent activity.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading dashboard...</p>
    </div>

    <div v-else class="dashboard-content">
      
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>
          <div class="metric-info">
            <div class="metric-label">Total Users</div>
            <div class="metric-value">{{ overview?.total_users || 0 }}</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon metric-icon--teal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
              <polyline points="9 22 9 12 15 12 15 22" />
            </svg>
          </div>
          <div class="metric-info">
            <div class="metric-label">Total Providers</div>
            <div class="metric-value">{{ overview?.total_providers || 0 }}</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon metric-icon--green">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
          <div class="metric-info">
            <div class="metric-label">Total Revenue</div>
            <div class="metric-value">{{ formatCurrency(overview?.total_revenue || 0) }}</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon metric-icon--pink">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
          </div>
          <div class="metric-info">
            <div class="metric-label">Pending Approvals</div>
            <div class="metric-value">{{ overview?.pending_approvals || 0 }}</div>
          </div>
        </div>
      </div>

      <div class="two-columns">
        <div class="col-left">
          <h2 class="section-title">Management</h2>
          <div class="cards">
            <div class="card" @click="goUsers">
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </div>
              <div class="card-body">
                <h3 class="card-title">Users</h3>
                <p class="card-desc">View and manage registered users</p>
              </div>
              <div class="card-arrow">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>
            </div>

            <div class="card" @click="goProviders">
              <div class="card-icon card-icon--teal">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                  <polyline points="9 22 9 12 15 12 15 22" />
                </svg>
              </div>
              <div class="card-body">
                <h3 class="card-title">Providers</h3>
                <p class="card-desc">Verify and manage service providers</p>
              </div>
              <div class="card-arrow">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>
            </div>

            <div class="card" @click="goCategories">
              <div class="card-icon card-icon--pink">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="14" y="14" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" />
                </svg>
              </div>
              <div class="card-body">
                <h3 class="card-title">Categories</h3>
                <p class="card-desc">Manage service categories</p>
              </div>
              <div class="card-arrow">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>
            </div>
          </div>

          <h2 class="section-title mt-8" v-if="pendingUsers.length > 0">Pending Users</h2>
          <div class="pending-list" v-if="pendingUsers.length > 0">
            <div class="pending-item" v-for="user in pendingUsers" :key="user.id">
              <div class="pending-info">
                <div class="pending-name">{{ user.full_name }}</div>
                <div class="pending-role">{{ user.role }} &bull; {{ user.email }}</div>
              </div>
              <button class="btn-review" @click="router.push(user.role === 'provider' ? '/admin/providers' : '/admin/users')">Review</button>
            </div>
          </div>
        </div>

        <div class="col-right">
          <h2 class="section-title">Recent Activity</h2>
          
          <div class="activity-block">
            <h3 class="activity-subtitle">Appointments</h3>
            <div class="activity-list" v-if="recentActivity?.recent_appointments?.length">
              <div class="activity-item" v-for="apt in recentActivity.recent_appointments" :key="apt.id">
                <div class="activity-dot"></div>
                <div class="activity-content">
                  <div class="activity-text"><span class="highlight">{{ apt.customer_name }}</span> booked <span class="highlight">{{ apt.service_name }}</span></div>
                  <div class="activity-subtext">with {{ apt.provider_name }} &bull; <span :class="['status-badge', 'status-' + apt.status]">{{ apt.status }}</span></div>
                  <div class="activity-time">{{ formatDate(apt.created_at) }}</div>
                </div>
              </div>
            </div>
            <div class="empty-state" v-else>No recent appointments</div>
          </div>

          <div class="activity-block mt-6">
            <h3 class="activity-subtitle">New Signups</h3>
            <div class="activity-list" v-if="recentActivity?.recent_users?.length">
              <div class="activity-item" v-for="user in recentActivity.recent_users" :key="user.id">
                <div class="activity-dot dot-teal"></div>
                <div class="activity-content">
                  <div class="activity-text"><span class="highlight">{{ user.full_name }}</span> joined</div>
                  <div class="activity-subtext">{{ user.role }} &bull; {{ user.email }}</div>
                  <div class="activity-time">{{ formatDate(user.created_at) }}</div>
                </div>
              </div>
            </div>
            <div class="empty-state" v-else>No recent signups</div>
          </div>

        </div>
      </div>

    </div>

  </div>
</template>

<style scoped src="../../styles/admin/AdminDashboardView.css"></style>