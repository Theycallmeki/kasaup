<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { useServiceStore } from "../../stores/serviceStore"
import { getCategories } from "../../services/categories"
import LocationPickerMap from "../../components/LocationPickerMap.vue"

const router = useRouter()
const serviceStore = useServiceStore()

const categories = ref<{ id: number; name: string }[]>([])
const categoriesLoading = ref(true)

const name = ref("")
const description = ref("")
const price = ref(0)
const duration_minutes = ref(60)
const category_id = ref<number | null>(null)

const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

function setLocation(data: any) {
  latitude.value = data.latitude
  longitude.value = data.longitude
}

onMounted(async () => {
  categoriesLoading.value = true
  try {
    const data = await getCategories({ limit: 500, offset: 0 })
    categories.value = Array.isArray(data) ? data : []
    if (categories.value.length) {
      const first = categories.value[0]
      if (category_id.value == null || !categories.value.some((c) => c.id === category_id.value)) {
        category_id.value = first.id
      }
    }
  } catch {
    categories.value = []
  } finally {
    categoriesLoading.value = false
  }
})

const createService = async () => {
  if (category_id.value == null) return
  try {
    await serviceStore.addService({
      category_id: category_id.value,
      name: name.value,
      description: description.value,
      price: price.value,
      duration_minutes: duration_minutes.value,
      latitude: latitude.value ?? undefined,
      longitude: longitude.value ?? undefined
    })
    router.push("/provider/services")
  } catch (err: any) {
    console.log(err.response?.data)
  }
}
</script>

<template>
  <div class="page">

    <div class="left-panel">
      <h1 class="title">Create Service</h1>

      <div class="form">

        <div class="field">
          <label for="svc-name">Service Name</label>
          <input
            id="svc-name"
            v-model="name"
            class="input"
            placeholder="e.g. Aircon Cleaning"
          />
        </div>

        <div class="field">
          <label for="svc-desc">Description</label>
          <textarea
            id="svc-desc"
            v-model="description"
            class="input"
            placeholder="Describe what's included..."
          />
        </div>

        <div class="field">
          <label for="svc-price">Price (₱)</label>
          <input
            id="svc-price"
            v-model.number="price"
            class="input"
            type="number"
            placeholder="0"
          />
        </div>

        <div class="field">
          <label for="svc-duration">Duration (minutes)</label>
          <input
            id="svc-duration"
            v-model.number="duration_minutes"
            class="input"
            type="number"
            placeholder="60"
          />
        </div>

        <div class="field">
          <label for="svc-category">Category</label>
          <select
            id="svc-category"
            v-model.number="category_id"
            class="input"
            :disabled="categoriesLoading || categories.length === 0"
          >
            <option v-if="categoriesLoading" disabled value="">Loading categories…</option>
            <option v-else-if="categories.length === 0" disabled value="">No categories available</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">
              {{ c.name }}
            </option>
          </select>
        </div>

        <p v-if="latitude && longitude" class="coords-hint">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
          </svg>
          {{ latitude.toFixed(5) }}, {{ longitude.toFixed(5) }}
        </p>

        <button
          class="submit-btn"
          type="button"
          :disabled="category_id == null || categories.length === 0"
          @click="createService"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Create Service
        </button>

      </div>
    </div>

    <div class="right-panel">
      <div class="map-header">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
        </svg>
        Click the map to set service location
      </div>
      <div class="map-wrap">
        <LocationPickerMap @location-selected="setLocation" />
      </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  display: flex;
  height: 100vh;
  background: #0e0c1a;
  font-family: 'DM Sans', sans-serif;
  overflow: hidden;
}

.left-panel {
  width: 380px;
  flex-shrink: 0;
  padding: 36px 28px;
  overflow-y: auto;
  border-right: 0.5px solid rgba(255, 255, 255, 0.07);
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.map-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.25);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 8px 12px 6px;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.map-wrap {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0 12px 12px;
}

.map-wrap :deep(.location-picker-root) {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.map-wrap :deep(#picker-map) {
  flex: 1;
  min-height: 0;
  height: auto !important;
  width: 100% !important;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 24px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.input {
  width: 100%;
  padding: 11px 13px;
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
  appearance: none;
  box-sizing: border-box;
}
.input::placeholder { color: rgba(255, 255, 255, 0.2); }
.input:focus { border-color: rgba(167, 139, 250, 0.5); }

textarea.input {
  resize: vertical;
  min-height: 80px;
}

select.input {
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.3)' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 13px center;
  padding-right: 34px;
}
select.input option {
  background: #1a1628;
  color: #fff;
}

.coords-hint {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: rgba(167, 139, 250, 0.7);
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: none;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s;
  margin-top: 4px;
}
.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}
.submit-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .page {
    flex-direction: column;
    height: auto;
    overflow: auto;
  }
  .left-panel {
    width: 100%;
    border-right: none;
    border-bottom: 0.5px solid rgba(255, 255, 255, 0.07);
  }
  .right-panel {
    min-height: 55vh;
    flex: 1;
  }
}
</style>