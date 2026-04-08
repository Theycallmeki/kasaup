<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { useServiceStore } from "../../stores/serviceStore"
import { getCategories } from "../../services/categories"
import { useLoading } from "../../hooks/useLoading"

const router = useRouter()
const serviceStore = useServiceStore()
const { startLoading, stopLoading } = useLoading()

const categories = ref<{ id: number; name: string }[]>([])
const categoriesLoading = ref(true)

const name = ref("")
const description = ref("")
const price = ref(0)
const duration_minutes = ref(60)
const category_id = ref<number | null>(null)

const imageFiles = ref<File[]>([])
const imagePreviews = ref<string[]>([])

onMounted(async () => {
  startLoading("Loading categories...")
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
    stopLoading()
  }
})

function onImagesChange(e: Event) {
  const files = Array.from((e.target as HTMLInputElement).files || [])
imageFiles.value = [...imageFiles.value, ...files]
imagePreviews.value = [
  ...imagePreviews.value,
  ...files.map(f => URL.createObjectURL(f))
]
}

function removeImage(index: number) {
  imageFiles.value = imageFiles.value.filter((_, i) => i !== index)
  imagePreviews.value = imagePreviews.value.filter((_, i) => i !== index)
}

const createService = async () => {
  if (category_id.value == null) return
  startLoading("Creating your service...")
  try {
    const service = await serviceStore.addService({
      category_id: category_id.value,
      name: name.value,
      description: description.value,
      price: price.value,
      duration_minutes: duration_minutes.value
    })

    if (imageFiles.value.length > 0) {
      await serviceStore.uploadImages(service.id, imageFiles.value)
    }

    router.push("/provider/services")
  } catch (err: any) {
    console.log(err.response?.data)
  } finally {
    stopLoading()
  }
}
</script>

<template>
  <div class="page">

    <div class="left-panel full">
      
      <div class="page-header">
        <p class="eyebrow">Service Management</p>
        <h1 class="title">Create Service</h1>
        <p class="hint">Fill in the details below to add a new service to your profile.</p>
      </div>

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

        <div class="field">
          <label>Service Images</label>
          <div class="images-wrap">
            <div v-if="imagePreviews.length" class="previews">
              <div
                v-for="(src, i) in imagePreviews"
                :key="i"
                class="preview-item"
              >
                <img :src="src" alt="preview" />
                <button class="remove-btn" type="button" @click="removeImage(i)">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
            <label class="image-btn" for="svc-images-input">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              {{ imageFiles.length ? `${imageFiles.length} file(s) selected` : "Upload Images" }}
            </label>
            <input
              id="svc-images-input"
              type="file"
              accept="image/*"
              multiple
              class="hidden-input"
              @change="onImagesChange"
            />
          </div>
        </div>

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

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  display: flex;
  min-height: 100vh;
  background: #0e0c1a;
  font-family: 'DM Sans', sans-serif;
}

.left-panel.full {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  padding: 36px 28px;
}

.page-header {
  margin-bottom: 28px;
}

.eyebrow {
  font-size: 11px;
  font-weight: 600;
  color: #a78bfa;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
}

.hint {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 18px;
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

.images-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.previews {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-item {
  position: relative;
  width: 72px;
  height: 72px;
  border-radius: 8px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
}

.image-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 16px;
  background: rgba(124, 58, 237, 0.15);
  border: 0.5px solid rgba(124, 58, 237, 0.4);
  border-radius: 8px;
  color: rgba(167, 139, 250, 0.9);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
  text-transform: none;
  letter-spacing: normal;
  width: fit-content;
}
.image-btn:hover {
  background: rgba(124, 58, 237, 0.25);
}

.hidden-input {
  display: none;
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
  margin-top: 12px;
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
  .left-panel.full {
    padding: 48px 20px 140px;
  }
}
</style>