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
@import "../../styles/provider/CreateServiceView.css";
</style>