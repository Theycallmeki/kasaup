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
    const res = await api.get("/users")
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
  await api.delete(`/users/${selectedUser.value.id}`)
  await fetchUsers()
  closeModal()
}
</script>

<template>
  <div class="user-page">

    <div class="user-header">
      <div>
        <h2>Users</h2>
        <p>View and manage registered users</p>
      </div>
    </div>

    <div v-if="loading" class="empty">
      Loading users...
    </div>

    <div v-else class="user-grid">

      <div
        v-for="user in users"
        :key="user.id"
        class="user-card"
        @click="openUser(user)"
      >
        <span class="role-badge" :class="user.role">
          {{ user.role }}
        </span>

        <h3 class="email">{{ user.email }}</h3>

        <p class="name">
          {{ user.full_name || "No name" }}
        </p>

        <div class="meta">
          <span>{{ user.phone || "No phone" }}</span>
        </div>
      </div>

    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">

        <span class="role-badge" :class="selectedUser?.role">
          {{ selectedUser?.role }}
        </span>

        <h3 class="modal-email">{{ selectedUser?.email }}</h3>

        <p class="modal-name">
          {{ selectedUser?.full_name || "No name" }}
        </p>

        <div class="modal-meta">
          <span>{{ selectedUser?.phone || "No phone" }}</span>
        </div>

        <div class="modal-actions">
          <button class="btn danger" @click="remove">
            Delete User
          </button>
          <button class="btn ghost" @click="closeModal">
            Close
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<style scoped>
.user-page {
  padding: 32px;
  background: #0b0f19;
  min-height: 100vh;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
}

.user-header {
  margin-bottom: 24px;
}

.user-header h2 {
  margin: 0;
  font-size: 20px;
}

.user-header p {
  margin: 4px 0 0;
  font-size: 13px;
  color: rgba(255,255,255,0.4);
}

.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 18px;
}

.user-card {
  cursor: pointer;
  position: relative;
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: all 0.2s ease;
}

.user-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0,0,0,0.4);
  border-color: rgba(124,58,237,0.3);
}

.role-badge {
  width: fit-content;
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.role-badge.admin {
  background: rgba(248,113,113,0.2);
  color: #f87171;
}

.role-badge.provider {
  background: rgba(56,189,248,0.2);
  color: #38bdf8;
}

.role-badge.user {
  background: rgba(167,139,250,0.2);
  color: #a78bfa;
}

.email {
  font-size: 14px;
  font-weight: 500;
  word-break: break-word;
}

.name {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

.meta {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
}

.empty {
  color: rgba(255,255,255,0.4);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(6px);
}

.modal {
  width: 320px;
  background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 18px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  animation: pop 0.2s ease;
}

.modal-email {
  font-size: 15px;
  font-weight: 500;
  margin-top: 6px;
}

.modal-name {
  font-size: 13px;
  color: rgba(255,255,255,0.6);
}

.modal-meta {
  font-size: 12px;
  color: rgba(255,255,255,0.4);
}

.modal-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
}

.btn.danger {
  background: rgba(248,113,113,0.2);
  color: #f87171;
}

.btn.danger:hover {
  background: rgba(248,113,113,0.3);
}

.btn.ghost {
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.6);
}

@keyframes pop {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>