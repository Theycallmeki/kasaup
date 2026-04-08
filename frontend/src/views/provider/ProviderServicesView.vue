<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useAuthStore } from "../../stores/authStore"
import { useScroll } from "../../hooks/useScroll"
import { useLoading } from "../../hooks/useLoading"
import api from "../../services/api"

const serviceStore = useServiceStore()
const authStore = useAuthStore()
const { startLoading, stopLoading } = useLoading()
const { scrollRef: pageScroll } = useScroll()

const providerId = ref<number | null>(null)
const editingId = ref<number | null>(null)
const imageFiles = ref<File[]>([])
const imagePreviews = ref<string[]>([])
const viewingImage = ref<string | null>(null)

const form = ref({
  name: "",
  description: "",
  price: 0,
  duration_minutes: 60,
  category_id: 1
})

const imgUrl = (path: string) => {
  if (!path) return ""
  if (path.startsWith("http")) return path
  return `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}`
}
  
onMounted(async () => {
  startLoading("Loading services...")
  try {
    await resolveProvider()
    await fetchServices()
  } finally {
    stopLoading()
  }
})

async function resolveProvider() {
  const res = await api.get("/providers/")
  const provider = res.data.find((p: any) => p.owner_id === authStore.user.id)
  providerId.value = provider?.id || null
}

async function fetchServices() {
  if (!providerId.value) return
  await serviceStore.fetchProviderServices(providerId.value)
}

function startEdit(service: any) {
  editingId.value = service.id
  imageFiles.value = []
  imagePreviews.value = []
  form.value = {
    name: service.name,
    description: service.description,
    price: service.price,
    duration_minutes: service.duration_minutes,
    category_id: service.category_id
  }
}

function cancelEdit() {
  editingId.value = null
  imageFiles.value = []
  imagePreviews.value = []
  resetForm()
}

function onImageChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files) return
  const files = Array.from(input.files)
  imageFiles.value = [...imageFiles.value, ...files]
  imagePreviews.value = [...imagePreviews.value, ...files.map(f => URL.createObjectURL(f))]
  input.value = ""
}

function removePreview(i: number) {
  imageFiles.value.splice(i, 1)
  imagePreviews.value.splice(i, 1)
}

async function removeExistingImage(serviceId: number, imageId: number) {
  startLoading("Removing image...")
  try {
    await serviceStore.removeServiceImage(serviceId, imageId)
    await fetchServices()
  } finally {
    stopLoading()
  }
}

async function saveEdit() {
  if (!editingId.value) return
  startLoading("Saving changes...")
  try {
    await serviceStore.editService(editingId.value, form.value)
    if (imageFiles.value.length) {
      await serviceStore.uploadImages(editingId.value, imageFiles.value)
    }
    editingId.value = null
    imageFiles.value = []
    imagePreviews.value = []
    resetForm()
    await fetchServices()
  } finally {
    stopLoading()
  }
}

async function deleteService(id: number) {
  startLoading("Deleting service...")
  try {
    await serviceStore.removeService(id)
    await fetchServices()
  } finally {
    stopLoading()
  }
}

function resetForm() {
  form.value = { name: "", description: "", price: 0, duration_minutes: 60, category_id: 1 }
}

function getService(id: number) {
  return serviceStore.services.find((s: any) => s.id === id)
}
</script>

<template>
  <div class="page" ref="pageScroll">

    <div class="page-header">
      <h1 class="title">My Services</h1>
      <router-link :to="{ name: 'createService' }" class="create-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        New Service
      </router-link>
    </div>

    <div v-if="serviceStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
      </svg>
      Loading services...
    </div>

    <div v-else-if="serviceStore.services.length === 0" class="state-msg">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:rgba(255,255,255,0.15);margin-bottom:12px">
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
      </svg>
      <p>No services yet.</p>
      <router-link :to="{ name: 'createService' }" class="empty-link">Create your first service</router-link>
    </div>

    <div v-else class="cards">
      <div
        v-for="service in serviceStore.services"
        :key="service.id"
        class="card"
        :class="{ 'card-editing': editingId === service.id }"
      >

        <!-- View mode -->
        <template v-if="editingId !== service.id">
          <div class="card-content">
            <div class="service-details">
              <div class="service-name">{{ service.name }}</div>
              <div class="service-meta">
                <span class="meta-pill">₱{{ service.price }}</span>
                <span class="meta-pill">{{ service.duration_minutes }} min</span>
              </div>
            </div>

            <div v-if="service.images?.length" class="service-images">
              <img
                v-for="img in service.images"
                :key="img.id"
                :src="imgUrl(img.image_url)"
                class="service-img"
                alt=""
                @click="viewingImage = imgUrl(img.image_url)"
                style="cursor: zoom-in;"
              />
            </div>
          </div>

          <div class="card-actions">
            <button class="action-btn btn-edit" @click="startEdit(service)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              Edit
            </button>
            <button class="action-btn btn-delete" @click="deleteService(service.id)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
              </svg>
              Delete
            </button>
          </div>
        </template>

        <!-- Edit mode -->
        <template v-else>
          <div class="edit-form">

            <div class="field">
              <label>Name</label>
              <input v-model="form.name" class="input" placeholder="Service name" />
            </div>

            <div class="field">
              <label>Description</label>
              <input v-model="form.description" class="input" placeholder="Description" />
            </div>

            <div class="field-row">
              <div class="field">
                <label>Price (₱)</label>
                <input v-model.number="form.price" class="input" type="number" placeholder="0" />
              </div>
              <div class="field">
                <label>Duration (min)</label>
                <input v-model.number="form.duration_minutes" class="input" type="number" placeholder="60" />
              </div>
            </div>

            <!-- Photos -->
            <div class="field">
              <label>Photos</label>

              <div class="photo-grid">
                <!-- Existing images -->
                <div
                  v-for="img in getService(editingId!)?.images ?? []"
                  :key="img.id"
                  class="img-wrap"
                >
                  <img :src="imgUrl(img.image_url)" class="preview-img" alt="" />
                  <button class="remove-img" @click="removeExistingImage(editingId!, img.id)">✕</button>
                </div>

                <!-- New image previews -->
                <div
                  v-for="(src, i) in imagePreviews"
                  :key="'new-' + i"
                  class="img-wrap"
                >
                  <img :src="src" class="preview-img" alt="" />
                  <button class="remove-img" @click="removePreview(i)">✕</button>
                </div>

                <!-- Add more button -->
                <label class="add-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                  <input type="file" accept="image/*" multiple class="file-input" @change="onImageChange" />
                </label>
              </div>
            </div>

            <div class="edit-actions">
              <button class="action-btn btn-save" @click="saveEdit">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Save
              </button>
              <button class="action-btn btn-cancel" @click="cancelEdit">
                Cancel
              </button>
            </div>

          </div>
        </template>

      </div>
    </div>

    <!-- Fullscreen Image Viewer -->
    <Teleport to="body">
      <div v-if="viewingImage" class="img-viewer-ov" @click="viewingImage = null">
        <button class="close-viewer">✕</button>
        <img :src="viewingImage" />
      </div>
    </Teleport>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: auto;
  background: #0e0c1a;
  padding: 36px 32px;
  padding-bottom: 200px;
  font-family: 'DM Sans', sans-serif;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 12px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: opacity 0.15s;
}
.create-btn:hover { opacity: 0.85; }

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.3);
  font-size: 14px;
  gap: 6px;
  text-align: center;
}
.empty-link {
  color: rgba(167, 139, 250, 0.8);
  font-size: 13px;
  text-decoration: none;
  margin-top: 4px;
}
.empty-link:hover { color: #a78bfa; }

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; margin-bottom: 8px; }

.cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  max-width: 1200px;
}

.card {
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px 18px;
  transition: border-color 0.2s;
}
.card:hover { border-color: rgba(167, 139, 250, 0.2); }
.card-editing { border-color: rgba(167, 139, 250, 0.3); }

.service-images {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  flex-shrink: 0;
}
.service-images::-webkit-scrollbar { display: none; }

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 16px;
}

.service-details {
  flex: 1;
}

.service-img {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 10px;
  border: 0.5px solid rgba(255,255,255,0.08);
  flex-shrink: 0;
}

.service-name {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
  font-family: inherit;
}

.service-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.meta-pill {
  font-size: 12px;
  color: rgba(167, 139, 250, 0.8);
  background: rgba(99, 60, 220, 0.15);
  border: 0.5px solid rgba(130, 90, 255, 0.2);
  border-radius: 100px;
  padding: 3px 10px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border-radius: 8px;
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.15s;
}
.action-btn:hover { opacity: 0.8; }

.btn-edit {
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}
.btn-delete {
  background: rgba(248, 113, 113, 0.08);
  border: 0.5px solid rgba(248, 113, 113, 0.25);
  color: rgba(248, 113, 113, 0.8);
}
.btn-save {
  background: rgba(52, 211, 153, 0.12);
  border: 0.5px solid rgba(52, 211, 153, 0.3);
  color: #34d399;
}
.btn-cancel {
  background: rgba(255, 255, 255, 0.04);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.4);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.input {
  width: 100%;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}
.input::placeholder { color: rgba(255, 255, 255, 0.2); }
.input:focus { border-color: rgba(167, 139, 250, 0.5); }

.file-input { display: none; }

.photo-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.img-wrap {
  position: relative;
}

.preview-img {
  width: 72px;
  height: 72px;
  object-fit: cover;
  border-radius: 10px;
  border: 0.5px solid rgba(255,255,255,0.08);
  display: block;
}

.remove-img {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(248, 113, 113, 0.9);
  border: none;
  color: #fff;
  font-size: 9px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.add-btn {
  width: 72px;
  height: 72px;
  border-radius: 10px;
  border: 0.5px dashed rgba(167, 139, 250, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(167, 139, 250, 0.5);
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
  text-transform: none;
  letter-spacing: 0;
  font-weight: 400;
}
.add-btn:hover {
  border-color: rgba(167, 139, 250, 0.6);
  color: rgba(167, 139, 250, 0.8);
}

.edit-actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

@media (max-width: 900px) {
  .cards { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .page { 
    padding: 24px 16px 220px; 
  }
  .field-row { grid-template-columns: 1fr; }
  .card-content { flex-direction: column; gap: 12px; }
  .service-images { width: 100%; overflow-x: auto; }
}
/* Image Viewer Lightbox */
.img-viewer-ov {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  cursor: zoom-out;
  animation: fadeIn 0.15s ease-out;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.img-viewer-ov img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.5);
}

.close-viewer {
  position: absolute;
  top: 24px;
  right: 24px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: background 0.2s;
  backdrop-filter: blur(4px);
}
.close-viewer:hover {
  background: rgba(255, 255, 255, 0.25);
}
</style>