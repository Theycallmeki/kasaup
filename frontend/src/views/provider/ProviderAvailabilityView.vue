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
import { useScroll } from "../../hooks/useScroll"
import { useLoading } from "../../hooks/useLoading"

const authStore = useAuthStore()
const { startLoading, stopLoading } = useLoading()
const { scrollRef: slotsScroll } = useScroll()
const { scrollRef: calendarScroll } = useScroll()

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
  startLoading("Loading your schedule...")
  try {
    const res = await api.get("/providers/")
    const provider = res.data.find((p: any) => p.owner_id === authStore.user.id)
    providerId.value = provider?.id || null

    if (providerId.value) {
      availability.value = await getAvailability(providerId.value)
    }
  } finally {
    stopLoading()
  }
})

async function submit() {
  if (!providerId.value) return
  startLoading(editingId.value ? "Updating slot..." : "Adding slot...")
  try {
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
  } finally {
    stopLoading()
  }
}

function edit(a: any) {
  editingId.value = a.id
  form.value = {
    day_of_week: a.day_of_week,
    start_time: formatTimeForInput(a.start_time),
    end_time: formatTimeForInput(a.end_time)
  }
}

async function remove(id: number) {
  startLoading("Removing slot...")
  try {
    await deleteAvailability(id)
    availability.value = await getAvailability(providerId.value!)
  } finally {
    stopLoading()
  }
}

function resetForm() {
  editingId.value = null
  form.value = {
    day_of_week: 0,
    start_time: "09:00",
    end_time: "17:00"
  }
}

function formatTimeForInput(timeStr: string) {
  if (!timeStr) return "09:00"
  if (timeStr.includes(':')) {
    const parts = timeStr.split(':')
    return `${parts[0].padStart(2, '0')}:${parts[1].padStart(2, '0')}`
  }
  return timeStr
}

const year = new Date().getFullYear()
const months = Array.from({ length: 12 }, (_, i) => i)

function getDaysInMonth(month: number) {
  return new Date(year, month + 1, 0).getDate()
}

function getFirstDayOfMonth(month: number) {
  return new Date(year, month, 1).getDay()
}

function formatDate(y: number, m: number, d: number) {
  return `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`
}

function getWeekdayForDate(y: number, m: number, d: number) {
  return new Date(y, m, d).getDay()
}

function hasAvailability(y: number, m: number, d: number) {
  const weekday = getWeekdayForDate(y, m, d)
  return availability.value.some(a => a.day_of_week === weekday)
}

const slotsForSelectedDate = computed(() => {
  if (!selectedDate.value) return []
  const [y, m, d] = selectedDate.value.split("-").map(Number)
  const weekday = getWeekdayForDate(y, m - 1, d)
  return availability.value.filter(a => a.day_of_week === weekday)
})

const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
const dayShort = ["S", "M", "T", "W", "T", "F", "S"]

function formatAmPm(timeStr: string): string {
  if (!timeStr) return timeStr
  const parts = timeStr.split(':').map(Number)
  let hours = parts[0]
  const minutes = parts[1] ?? 0
  const ampm = hours >= 12 ? 'PM' : 'AM'
  hours = hours % 12 || 12
  return `${hours}:${String(minutes).padStart(2, '0')} ${ampm}`
}
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

        <div class="slots-list" ref="slotsScroll">
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
              <div class="slot-time">{{ formatAmPm(slot.start_time) }} - {{ formatAmPm(slot.end_time) }}</div>
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
        <div class="panel-header">
          <div class="ph-left">
            <h2 class="section-title">Yearly Overview</h2>
            <div class="year-badge">{{ year }}</div>
          </div>
          <button class="today-btn" @click="selectedDate = formatDate(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())">
            Go to Today
          </button>
        </div>
        
        <div class="months-grid" ref="calendarScroll">
          <div v-for="month in months" :key="month" class="month-card">
            <div class="month-name">{{ new Date(year, month).toLocaleString("default", { month: "long" }) }}</div>
            <div class="days-grid">
              <div v-for="d in dayShort" :key="'label-'+d" class="day-label cell-shared">{{ d }}</div>
              
              <!-- Empty cells for alignment -->
              <div v-for="empty in getFirstDayOfMonth(month)" :key="'empty-'+empty" class="day-cell empty cell-shared"></div>
              
              <!-- Real day cells -->
              <div
                v-for="day in getDaysInMonth(month)"
                :key="day"
                class="day-cell cell-shared"
                :class="{
                  'has-slot': hasAvailability(year, month, day),
                  'selected': selectedDate === formatDate(year, month, day),
                  'is-today': formatDate(year, month, day) === formatDate(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())
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
              {{ formatAmPm(slot.start_time) }} - {{ formatAmPm(slot.end_time) }}
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
  min-height: auto;
  background: #0e0c1a;
  padding: 36px 32px;
  padding-bottom: 200px;
  font-family: 'DM Sans', sans-serif;
  color: #fff;
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
  padding: 0 14px;
  height: 42px;
  font-size: 14px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  color-scheme: dark;
  transition: border-color 0.2s;
  -webkit-appearance: none;
  appearance: none;
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

.calendar-panel {
  flex: 2;
  display: flex;
  flex-direction: column;
}

.calendar-panel .panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.ph-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.today-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.today-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(167, 139, 250, 0.4);
}

.year-badge {
  background: rgba(167, 139, 250, 0.15);
  color: #a78bfa;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  border: 1px solid rgba(167, 139, 250, 0.2);
}

.months-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

/* ✅ FIX: increased horizontal padding so Saturday dates don't hug the border */
.month-card {
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 18px 20px;
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.month-card:hover {
  border-color: rgba(167, 139, 250, 0.2);
  background: rgba(255, 255, 255, 0.035);
}

.month-name {
  font-family: 'Sora', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 16px;
  text-transform: capitalize;
  letter-spacing: 0.02em;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  width: 100%;
  justify-items: center;
}

.cell-shared {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.day-label {
  font-size: 10px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.3);
  text-align: center;
  border: 1px solid transparent;
}

.day-cell {
  background: transparent;
  width: 100%;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

.day-cell:hover:not(.empty) {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  transform: translateY(-1px);
}

.day-cell.empty {
  cursor: default;
}

.day-cell.is-today {
  color: #a78bfa;
  font-weight: 700;
  position: relative;
}

.day-cell.is-today::after {
  content: '';
  position: absolute;
  bottom: 4px;
  width: 3px;
  height: 3px;
  background: #a78bfa;
  border-radius: 50%;
}

.day-cell.has-slot {
  background: rgba(124, 58, 237, 0.15);
  color: #c4b5fd;
  border: 1px solid rgba(124, 58, 237, 0.15);
}

.day-cell.has-slot:hover {
  background: rgba(124, 58, 237, 0.3);
  border-color: rgba(124, 58, 237, 0.4);
}

.day-cell.selected {
  background: #7c3aed !important;
  border: 1px solid #a78bfa !important;
  color: #fff !important;
  box-shadow: 0 0 15px rgba(124, 58, 237, 0.4);
  transform: scale(1.15);
  z-index: 2;
  font-weight: 700;
}

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

/* --- Responsiveness --- */

/* Tablet & Smaller Desktop */
@media (max-width: 1024px) {
  .layout-grid {
    gap: 20px;
  }
  
  .months-grid {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }
}

/* Mobile & Small Tablets */
@media (max-width: 900px) {
  .page { 
    padding: 24px 16px 140px; 
  }
  
  .layout-grid {
    flex-direction: column;
  }
  
  .schedule-card, 
  .calendar-panel {
    max-width: 100%;
    width: 100%;
  }

  .months-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

/* Phones */
@media (max-width: 600px) {
  .field-row {
    flex-direction: column;
    gap: 16px;
  }

  .month-card {
    padding: 14px 12px;
  }

  .days-grid {
    gap: 2px;
  }

  .day-cell {
    font-size: 10px;
  }

  .title {
    font-size: 1.3rem;
  }

  .selected-date-panel {
    padding: 16px;
  }

  .date-title {
    font-size: 1rem;
  }
}

/* Extra Small Phones */
@media (max-width: 380px) {
  .months-grid {
    grid-template-columns: 1fr;
  }
  
  .page {
    padding: 20px 12px 120px;
  }
}
</style>