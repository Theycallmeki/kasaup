<script setup lang="ts">
import { onMounted, ref, computed } from "vue"
import api from "../../services/api"

const users = ref<any[]>([])
const loading = ref(false)

const selectedUser = ref<any | null>(null)
const showModal = ref(false)

const activeTab = ref<"all" | "pending">("all")

const showRejectConfirm = ref(false)
const rejectingUser = ref<any | null>(null)
const actionLoading = ref<number | null>(null)

onMounted(fetchUsers)

async function fetchUsers() {
  loading.value = true
  try {
    const res = await api.get("/users/")
    users.value = res.data
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  if (activeTab.value === "pending") {
    return users.value.filter(u => u.role === "provider" && !u.is_approved)
  }
  return users.value
})

const pendingCount = computed(() => {
  return users.value.filter(u => u.role === "provider" && !u.is_approved).length
})

function openUser(user: any) {
  selectedUser.value = user
  showModal.value = true
}

function closeModal() {
  selectedUser.value = null
  showModal.value = false
}

async function remove() {
  if (!selectedUser.value) return
  await api.delete(`/users/${selectedUser.value.id}/`)
  await fetchUsers()
  closeModal()
}

async function approveUser(user: any) {
  actionLoading.value = user.id
  try {
    await api.put(`/users/${user.id}/approve/`)
    await fetchUsers()
  } catch (err) {
    alert("Failed to approve user")
  } finally {
    actionLoading.value = null
  }
}

function confirmReject(user: any) {
  rejectingUser.value = user
  showRejectConfirm.value = true
}

async function handleReject() {
  if (!rejectingUser.value) return
  actionLoading.value = rejectingUser.value.id
  try {
    await api.put(`/users/${rejectingUser.value.id}/reject/`)
    await fetchUsers()
    showRejectConfirm.value = false
    rejectingUser.value = null
  } catch (err) {
    alert("Failed to reject user")
  } finally {
    actionLoading.value = null
  }
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <div>
        <div class="header-label">Admin</div>
        <h1 class="title">Users</h1>
        <p class="hint">View and manage registered users on the platform.</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button 
        class="tab" 
        :class="{ active: activeTab === 'all' }" 
        @click="activeTab = 'all'"
      >
        All Users
      </button>
      <button 
        class="tab" 
        :class="{ active: activeTab === 'pending' }" 
        @click="activeTab = 'pending'"
      >
        Pending Approval
        <span v-if="pendingCount > 0" class="tab-badge">{{ pendingCount }}</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <span class="spinner"></span>
      <p>Loading users...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="!filteredUsers.length" class="state-msg empty">
      <div class="empty-icon">
        <svg v-if="activeTab === 'pending'" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        <svg v-else width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      </div>
      <h3 class="empty-text">{{ activeTab === 'pending' ? 'No pending approvals' : 'No users found' }}</h3>
      <p class="empty-sub">{{ activeTab === 'pending' ? 'All provider applications have been reviewed.' : 'Registered users will appear here.' }}</p>
    </div>

    <!-- Grid -->
    <div v-else class="user-grid">
      <div
        v-for="user in filteredUsers"
        :key="user.id"
        class="user-card"
        :class="{ 'pending-card': user.role === 'provider' && !user.is_approved }"
        @click="openUser(user)"
      >
        <div class="card-top">
          <div class="avatar">{{ (user.full_name || user.email || '?').charAt(0).toUpperCase() }}</div>
          <div class="badge-row">
            <span 
              v-if="user.role === 'provider' && !user.is_approved" 
              class="status-badge pending"
            >
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              Pending
            </span>
            <span class="role-badge" :class="user.role">{{ user.role }}</span>
          </div>
        </div>

        <h3 class="email">{{ user.email }}</h3>
        <p class="name">{{ user.full_name || 'No name' }}</p>

        <div class="meta">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.18h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.81a16 16 0 0 0 6 6l.94-.94a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 21.69 16z"/>
          </svg>
          {{ user.phone || 'No phone' }}
        </div>

        <!-- Approval Actions (inline, only for pending) -->
        <div v-if="user.role === 'provider' && !user.is_approved" class="approval-actions" @click.stop>
          <button 
            class="action-inline action-approve" 
            :disabled="actionLoading === user.id"
            @click="approveUser(user)"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            {{ actionLoading === user.id ? 'Processing...' : 'Approve' }}
          </button>
          <button 
            class="action-inline action-reject"
            :disabled="actionLoading === user.id"
            @click="confirmReject(user)"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Reject
          </button>
        </div>
      </div>
    </div>

    <!-- User Detail Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <div class="modal-avatar">
              {{ (selectedUser?.full_name || selectedUser?.email || '?').charAt(0).toUpperCase() }}
            </div>
            <div class="modal-header-text">
              <div class="badge-row">
                <span 
                  v-if="selectedUser?.role === 'provider' && !selectedUser?.is_approved" 
                  class="status-badge pending"
                >Pending</span>
                <span class="role-badge" :class="selectedUser?.role">{{ selectedUser?.role }}</span>
              </div>
              <h3 class="modal-email">{{ selectedUser?.email }}</h3>
              <p class="modal-name">{{ selectedUser?.full_name || 'No name' }}</p>
            </div>
          </div>

          <div class="modal-divider"></div>

          <div class="modal-details">
            <div class="detail-row">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.18h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.81a16 16 0 0 0 6 6l.94-.94a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 21.69 16z"/>
              </svg>
              <span>{{ selectedUser?.phone || 'No phone' }}</span>
            </div>
          </div>

          <div class="modal-actions">
            <button 
              v-if="selectedUser?.role === 'provider' && !selectedUser?.is_approved"
              class="btn btn-approve" 
              @click="approveUser(selectedUser); closeModal()"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              Approve
            </button>
            <button class="btn btn-danger" @click="remove">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                <path d="M10 11v6"/><path d="M14 11v6"/>
                <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
              </svg>
              Delete User
            </button>
            <button class="btn btn-ghost" @click="closeModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Reject Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showRejectConfirm" class="modal-overlay" @click.self="showRejectConfirm = false">
        <div class="modal">
          <div class="modal-header" style="margin-bottom: 12px;">
            <div class="modal-avatar reject-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
              </svg>
            </div>
            <div class="modal-header-text">
              <h3 class="modal-email">Reject Provider?</h3>
              <p class="modal-name">{{ rejectingUser?.full_name || rejectingUser?.email }}</p>
            </div>
          </div>
          <p style="color: rgba(255,255,255,0.5); font-size: 13px; line-height: 1.6; margin: 0 0 20px;">
            This will <strong style="color: #f87171;">permanently delete</strong> their account and send a rejection email to 
            <strong style="color: #fff;">{{ rejectingUser?.email }}</strong>.
          </p>
          <div class="modal-actions">
            <button class="btn btn-danger" @click="handleReject">
              Reject & Delete
            </button>
            <button class="btn btn-ghost" @click="showRejectConfirm = false">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<style scoped src="@/styles/admin/AdminUsersView.css"></style>