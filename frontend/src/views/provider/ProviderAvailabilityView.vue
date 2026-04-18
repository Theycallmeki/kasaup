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

<style src="../../styles/provider/ProviderAvailabilityView.css" scoped></style>