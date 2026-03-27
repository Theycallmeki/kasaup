<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useAuthStore } from "../../stores/authStore"
import api from "../../services/api"
import {
  getAvailability,
  createAvailability,
  updateAvailability,
  deleteAvailability
} from "../../services/availability"

const authStore = useAuthStore()

const availability = ref<any[]>([])
const loading = ref(false)

const providerId = ref<number | null>(null)

const form = ref({
  day_of_week: 0,
  start_time: "09:00",
  end_time: "17:00"
})

const editingId = ref<number | null>(null)

onMounted(async () => {
  await resolveProvider()
  await fetchAvailability()
})

async function resolveProvider() {
  const res = await api.get("/providers")
  const provider = res.data.find(
    (p: any) => p.owner_id === authStore.user.id
  )
  providerId.value = provider?.id || null
}

async function fetchAvailability() {
  if (!providerId.value) return
  loading.value = true
  try {
    availability.value = await getAvailability(providerId.value)
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!providerId.value) return
  if (editingId.value) {
    await updateAvailability(editingId.value, form.value)
  } else {
    await createAvailability({
      provider_id: providerId.value,
      ...form.value
    })
  }
  resetForm()
  await fetchAvailability()
}

function edit(a: any) {
  editingId.value = a.id
  form.value = {
    day_of_week: a.day_of_week,
    start_time: a.start_time,
    end_time: a.end_time
  }
}

async function remove(id: number) {
  await deleteAvailability(id)
  await fetchAvailability()
}

function resetForm() {
  editingId.value = null
  form.value = {
    day_of_week: 0,
    start_time: "09:00",
    end_time: "17:00"
  }
}

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">Provider Availability</h1>
      <p class="hint">Set your weekly schedule so customers can book you.</p>
    </div>

    <div class="form-card">
      <p class="form-label">{{ editingId ? "Edit Slot" : "Add New Slot" }}</p>

      <form class="availability-form" @submit.prevent="submit">
        <select v-model.number="form.day_of_week" class="field">
          <option v-for="(day, i) in days" :key="i" :value="i">{{ day }}</option>
        </select>

        <input type="time" v-model="form.start_time" class="field" />
        <input type="time" v-model="form.end_time" class="field" />

        <div class="form-actions">
          <button type="submit" class="submit-btn">
            {{ editingId ? "Update" : "Add Slot" }}
          </button>
          <button v-if="editingId" type="button" class="cancel-edit-btn" @click="resetForm">
            Cancel
          </button>
        </div>
      </form>
    </div>

    <div class="card-divider" />

    <div v-if="loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
      Loading availability...
    </div>

    <div v-else-if="availability.length === 0" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <rect x="3" y="4" width="18" height="18" rx="2"/>
        <line x1="16" y1="2" x2="16" y2="6"/>
        <line x1="8" y1="2" x2="8" y2="6"/>
        <line x1="3" y1="10" x2="21" y2="10"/>
      </svg>
      <p>No availability slots yet.</p>
    </div>

    <div v-else class="slots">
      <div
        v-for="slot in availability"
        :key="slot.id"
        class="slot-card"
      >
        <div class="slot-left">
          <div class="slot-day">{{ days[(slot.day_of_week + 1) % 7] }}</div>
          <div class="slot-time">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
            {{ slot.start_time }} – {{ slot.end_time }}
          </div>
        </div>

        <div class="slot-actions">
          <button class="edit-btn" @click="edit(slot)">Edit</button>
          <button class="delete-btn" @click="remove(slot.id)">Delete</button>
        </div>
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
  margin-bottom: 28px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}

.form-card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-label {
  font-size: 12px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin: 0 0 14px;
}

.availability-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.field {
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 13px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  outline: none;
  color-scheme: dark;
  -webkit-appearance: none;
  appearance: none;
}

.field:focus {
  border-color: rgba(167, 139, 250, 0.5);
}

.field option {
  background: #1a1728;
  color: #fff;
}

.form-actions {
  display: flex;
  gap: 8px;
}

.submit-btn {
  font-size: 13px;
  font-weight: 500;
  padding: 9px 18px;
  border-radius: 8px;
  background: rgba(124, 58, 237, 0.35);
  border: 0.5px solid rgba(124, 58, 237, 0.5);
  color: #fff;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.submit-btn:hover {
  background: rgba(124, 58, 237, 0.5);
}

.cancel-edit-btn {
  font-size: 13px;
  font-weight: 500;
  padding: 9px 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.cancel-edit-btn:hover {
  opacity: 0.8;
}

.card-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin-bottom: 20px;
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
  gap: 6px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 1s linear infinite;
  margin-bottom: 8px;
}

.slots {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.slot-card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slot-day {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 4px;
}

.slot-time {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
}

.slot-actions {
  display: flex;
  gap: 8px;
}

.edit-btn {
  font-size: 13px;
  font-weight: 500;
  padding: 7px 14px;
  border-radius: 8px;
  background: rgba(96, 165, 250, 0.1);
  border: 0.5px solid rgba(96, 165, 250, 0.25);
  color: #60a5fa;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.edit-btn:hover {
  opacity: 0.8;
}

.delete-btn {
  font-size: 13px;
  font-weight: 500;
  padding: 7px 14px;
  border-radius: 8px;
  background: rgba(248, 113, 113, 0.08);
  border: 0.5px solid rgba(248, 113, 113, 0.25);
  color: rgba(248, 113, 113, 0.8);
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}

.delete-btn:hover {
  opacity: 0.8;
}

@media (max-width: 640px) {
  .page {
    padding: 24px 16px;
  }

  .availability-form {
    flex-direction: column;
    align-items: stretch;
  }

  .slot-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>