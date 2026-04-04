<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
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
const providerId = ref<number | null>(null)

const form = ref({
  day_of_week: 0,
  start_time: "09:00",
  end_time: "17:00"
})

const editingId = ref<number | null>(null)
const selectedDate = ref("")
const showDropdown = ref(false)

onMounted(async () => {
  const res = await api.get("/providers/")
  const provider = res.data.find((p: any) => p.owner_id === authStore.user.id)
  providerId.value = provider?.id || null

  if (providerId.value) {
    availability.value = await getAvailability(providerId.value)
  }
})

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
  availability.value = await getAvailability(providerId.value!)
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
  availability.value = await getAvailability(providerId.value!)
}

function resetForm() {
  editingId.value = null
  form.value = {
    day_of_week: 0,
    start_time: "09:00",
    end_time: "17:00"
  }
}

const year = new Date().getFullYear()
const months = Array.from({ length: 12 }, (_, i) => i)

function getDaysInMonth(month: number) {
  return new Date(year, month + 1, 0).getDate()
}

function formatDate(y: number, m: number, d: number) {
  return `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`
}

function getWeekday(date: string) {
  return new Date(date).getDay()
}

function hasAvailability(date: string) {
  const weekday = getWeekday(date)
  return availability.value.some(a => a.day_of_week === weekday)
}

const slotsForSelectedDate = computed(() => {
  if (!selectedDate.value) return []
  const weekday = getWeekday(selectedDate.value)
  return availability.value.filter(a => a.day_of_week === weekday)
})

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
</script>

<template>
  <div class="page">
    <div class="page-header">
      <h1 class="title">Availability</h1>
      <p class="hint">Set your weekly schedule and verify your calendar representation.</p>
    </div>

    <div class="layout-grid">
      
      <!-- Left Column: Weekly Schedule -->
      <div class="card schedule-card">
        <h2 class="section-title">Weekly Schedule</h2>
        
        <form class="schedule-form" @submit.prevent="submit">
          <div class="field-group">
            <label class="field-label">Day of Week</label>
            <div class="custom-select-wrapper" tabindex="0" @blur="showDropdown = false">
              <div class="field custom-select" @click="showDropdown = !showDropdown">
                <span>{{ days[form.day_of_week] }}</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ rotated: showDropdown }">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
              <Transition name="dropdown">
                <div v-show="showDropdown" class="custom-select-options">
                  <div v-for="(day,i) in days" :key="i" 
                       @click="form.day_of_week = i; showDropdown = false" 
                       class="custom-select-option" 
                       :class="{ active: form.day_of_week === i }">
                    {{ day }}
                  </div>
                </div>
              </Transition>
            </div>
          </div>

          <div class="field-row">
            <div class="field-group">
              <label class="field-label">Start Time</label>
              <input type="time" v-model="form.start_time" class="field time-field" />
            </div>
            <div class="field-group">
              <label class="field-label">End Time</label>
              <input type="time" v-model="form.end_time" class="field time-field" />
            </div>
          </div>

          <button type="submit" class="action-btn">
            {{ editingId ? "Update Slot" : "Add Slot" }}
          </button>
        </form>

        <div class="card-divider" />

        <div class="slots-list">
          <div v-if="availability.length === 0" class="empty-state">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            No slots set up yet.
          </div>
          
          <div v-for="slot in availability" :key="slot.id" class="slot-item">
            <div class="slot-info">
              <div class="slot-day">{{ days[slot.day_of_week] }}</div>
              <div class="slot-time">{{ slot.start_time }} - {{ slot.end_time }}</div>
            </div>
            <div class="slot-actions">
              <button class="icon-btn edit-btn" @click.prevent="edit(slot)" title="Edit">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
              </button>
              <button class="icon-btn delete-btn" @click.prevent="remove(slot.id)" title="Delete">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Calendar Overview -->
      <div class="calendar-panel">
        <h2 class="section-title">Yearly Overview</h2>
        
        <div class="months-grid">
          <div v-for="month in months" :key="month" class="month-card">
            <div class="month-name">{{ new Date(year, month).toLocaleString("default", { month: "short" }) }}</div>
            <div class="days-grid">
              <div
                v-for="day in getDaysInMonth(month)"
                :key="day"
                class="day-cell"
                :class="{
                  'has-slot': hasAvailability(formatDate(year, month, day)),
                  'selected': selectedDate === formatDate(year, month, day)
                }"
                @click="selectedDate = formatDate(year, month, day)"
              >
                {{ day }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedDate" class="selected-date-panel">
          <div class="selected-date-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: #a78bfa;">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <h3 class="date-title">
              {{ new Date(selectedDate).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) }}
            </h3>
          </div>
          
          <div v-if="!slotsForSelectedDate.length" class="empty-state mini">
            No availability for this date based on your weekly schedule.
          </div>
          <div v-else class="day-slots-grid">
            <div v-for="slot in slotsForSelectedDate" :key="slot.id" class="day-slot-pill">
              {{ slot.start_time }} - {{ slot.end_time }}
            </div>
          </div>
        </div>
      </div>

    </div>
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
  margin-bottom: 28px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 8px;
}

.hint {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.layout-grid {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.section-title {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 20px;
  color: #fff;
}

/* Glass Card Global Styles */
.card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
}

.card-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin: 24px 0;
}

/* Schedule Column */
.schedule-card {
  flex: 1;
  max-width: 400px;
  display: flex;
  flex-direction: column;
}

.schedule-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.field-row {
  display: flex;
  gap: 12px;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.field {
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  color-scheme: dark;
  transition: border-color 0.2s;
}

.field:focus {
  border-color: rgba(167, 139, 250, 0.5);
}

.custom-select-wrapper {
  position: relative;
  outline: none;
}

.custom-select {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.custom-select svg {
  transition: transform 0.2s ease;
  color: rgba(255, 255, 255, 0.4);
}

.custom-select svg.rotated {
  transform: rotate(180deg);
}

.custom-select-options {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #13111f;
  border: 0.5px solid rgba(167, 139, 250, 0.3);
  border-radius: 8px;
  overflow: hidden;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.custom-select-option {
  padding: 10px 14px;
  font-size: 14px;
  color: #fff;
  cursor: pointer;
  transition: background 0.15s;
}

.custom-select-option:hover {
  background: rgba(255, 255, 255, 0.05);
}

.custom-select-option.active {
  background: rgba(124, 58, 237, 0.25);
  color: #c4b5fd;
  font-weight: 500;
}

.dropdown-enter-active, .dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.action-btn {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 20px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: 1px solid rgba(167, 139, 250, 0.6);
  color: #fff;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: filter 0.2s, transform 0.1s;
}

.action-btn:hover {
  filter: brightness(1.1);
}

.action-btn:active {
  transform: scale(0.98);
}

/* Slots List */
.slots-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
  border-radius: 12px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
  gap: 12px;
}

.empty-state.mini {
  padding: 24px;
  border: none;
  background: rgba(255, 255, 255, 0.02);
}

.slot-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  transition: border-color 0.2s, background 0.2s;
}

.slot-item:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(167, 139, 250, 0.3);
}

.slot-day {
  font-weight: 600;
  font-size: 14px;
  color: #e5e7eb;
}

.slot-time {
  font-size: 13px;
  color: rgba(167, 139, 250, 0.9);
  margin-top: 2px;
}

.slot-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.edit-btn:hover { color: #34d399; }
.delete-btn:hover { color: #ef4444; }

/* Calendar Column */
.calendar-panel {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.months-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.month-card {
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 14px;
}

.month-name {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.day-cell {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.day-cell:hover {
  background: rgba(255, 255, 255, 0.1);
}

.day-cell.has-slot {
  background: rgba(124, 58, 237, 0.2);
  color: #c4b5fd;
}

.day-cell.has-slot:hover {
  background: rgba(124, 58, 237, 0.4);
}

.day-cell.selected {
  background: rgba(124, 58, 237, 0.5);
  border-color: #a855f7;
  color: #fff;
  transform: scale(1.1);
  z-index: 2;
}

/* Selected Day Panel */
.selected-date-panel {
  margin-top: 24px;
  background: rgba(124, 58, 237, 0.08);
  border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 16px;
  padding: 24px;
}

.selected-date-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.date-title {
  font-family: 'Sora', sans-serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.day-slots-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.day-slot-pill {
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(167, 139, 250, 0.4);
  border-radius: 100px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #e5e7eb;
}

/* Responsive */
@media (max-width: 900px) {
  .layout-grid {
    flex-direction: column;
  }
  .schedule-card, .calendar-panel {
    max-width: 100%;
    width: 100%;
  }
}
</style>