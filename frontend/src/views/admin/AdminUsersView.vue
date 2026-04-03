<script setup lang="ts">
import { onMounted, ref } from "vue"
import api from "../../services/api"

const users = ref<any[]>([])
const loading = ref(false)

const selectedUser = ref<any | null>(null)
const showModal = ref(false)

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

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <span class="spinner"></span>
      <p>Loading users...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="!users.length" class="state-msg empty">
      <div class="empty-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      </div>
      <h3 class="empty-text">No users found</h3>
      <p class="empty-sub">Registered users will appear here.</p>
    </div>

    <!-- Grid -->
    <div v-else class="user-grid">
      <div
        v-for="user in users"
        :key="user.id"
        class="user-card"
        @click="openUser(user)"
      >
        <div class="card-top">
          <div class="avatar">{{ (user.full_name || user.email || '?').charAt(0).toUpperCase() }}</div>
          <span class="role-badge" :class="user.role">{{ user.role }}</span>
        </div>

        <h3 class="email">{{ user.email }}</h3>

        <p class="name">{{ user.full_name || 'No name' }}</p>

        <div class="meta">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.18h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.81a16 16 0 0 0 6 6l.94-.94a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 21.69 16z"/>
          </svg>
          {{ user.phone || 'No phone' }}
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">

          <div class="modal-header">
            <div class="modal-avatar">
              {{ (selectedUser?.full_name || selectedUser?.email || '?').charAt(0).toUpperCase() }}
            </div>
            <div class="modal-header-text">
              <span class="role-badge" :class="selectedUser?.role">{{ selectedUser?.role }}</span>
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

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
  color: #fff;
}

.page-header {
  margin-bottom: 32px;
}

.header-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(167, 139, 250, 0.6);
  margin-bottom: 6px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
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
  background: rgba(255, 255, 255, 0.015);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}
.empty-icon { color: rgba(167, 139, 250, 0.5); margin-bottom: 4px; }
.empty-text {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem;
  color: #fff;
  margin: 0;
}
.empty-sub { margin: 4px 0 0; font-size: 13px; }

@keyframes spin { to { transform: rotate(360deg); } }
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #a78bfa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Grid */
.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
}

/* Card */
.user-card {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.025);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: border-color 0.2s, background 0.2s;
}
.user-card:hover {
  border-color: rgba(167, 139, 250, 0.3);
  background: rgba(255, 255, 255, 0.04);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(99, 60, 220, 0.5), rgba(130, 90, 255, 0.5));
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  color: #fff;
  flex-shrink: 0;
}

.role-badge {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 100px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.role-badge.admin {
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
  border: 0.5px solid rgba(248, 113, 113, 0.3);
}
.role-badge.provider {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 0.5px solid rgba(56, 189, 248, 0.3);
}
.role-badge.user {
  background: rgba(167, 139, 250, 0.15);
  color: #a78bfa;
  border: 0.5px solid rgba(167, 139, 250, 0.3);
}

.email {
  font-size: 13.5px;
  font-weight: 500;
  color: #fff;
  word-break: break-word;
  margin: 0;
}

.name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.45);
  margin: 0;
}

.meta {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
  margin-top: 2px;
}

/* Modal */
@keyframes pop {
  from { transform: scale(0.94) translateY(8px); opacity: 0; }
  to   { transform: scale(1) translateY(0); opacity: 1; }
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
  z-index: 100;
}

.modal {
  width: 340px;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 0;
  animation: pop 0.2s ease;
  backdrop-filter: blur(20px);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 20px;
}

.modal-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(99, 60, 220, 0.6), rgba(130, 90, 255, 0.6));
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 1.2rem;
  color: #fff;
  flex-shrink: 0;
  border: 0.5px solid rgba(130, 90, 255, 0.4);
}

.modal-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.modal-email {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin: 0;
  word-break: break-word;
}

.modal-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.modal-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin-bottom: 16px;
}

.modal-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}
.detail-row svg { flex-shrink: 0; color: rgba(167, 139, 250, 0.6); }

.modal-actions {
  display: flex;
  gap: 8px;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 12px;
  border-radius: 10px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  border: 0.5px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}

.btn-danger {
  background: rgba(248, 113, 113, 0.12);
  border-color: rgba(248, 113, 113, 0.25);
  color: #f87171;
}
.btn-danger:hover {
  background: rgba(248, 113, 113, 0.2);
  border-color: rgba(248, 113, 113, 0.4);
}

.btn-ghost {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.5);
}
.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
}

@media (max-width: 640px) {
  .page { padding: 24px 16px; }
  .user-grid { grid-template-columns: 1fr; }
}
</style>