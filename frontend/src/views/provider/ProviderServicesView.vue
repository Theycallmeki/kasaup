<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue"
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
const deleteConfirmId = ref<number | null>(null)

// Gallery viewer
const galleryImages = ref<string[]>([])
const galleryIndex = ref(0)
const viewingGallery = computed(() => galleryImages.value.length > 0)

function openGallery(images: any[], startIndex = 0) {
  galleryImages.value = images.map((img: any) => imgUrl(img.image_url))
  galleryIndex.value = startIndex
}

function closeGallery() {
  galleryImages.value = []
  galleryIndex.value = 0
}

function galleryNext() {
  galleryIndex.value = (galleryIndex.value + 1) % galleryImages.value.length
}

function galleryPrev() {
  galleryIndex.value = (galleryIndex.value - 1 + galleryImages.value.length) % galleryImages.value.length
}

function onGalleryKey(e: KeyboardEvent) {
  if (!viewingGallery.value) return
  if (e.key === 'Escape') closeGallery()
  if (e.key === 'ArrowRight') galleryNext()
  if (e.key === 'ArrowLeft') galleryPrev()
}

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
  window.addEventListener('keydown', onGalleryKey)
  try {
    await resolveProvider()
    await fetchServices()
  } finally {
    stopLoading()
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', onGalleryKey)
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
  deleteConfirmId.value = null
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

    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="title">My Services</h1>
        <span class="service-count" v-if="serviceStore.services.length">
          {{ serviceStore.services.length }} {{ serviceStore.services.length === 1 ? 'service' : 'services' }}
        </span>
      </div>
      <router-link :to="{ name: 'createService' }" class="create-btn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        New Service
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="serviceStore.loading" class="state-msg">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
      </svg>
      Loading services...
    </div>

    <!-- Empty state -->
    <div v-else-if="serviceStore.services.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
        </svg>
      </div>
      <p class="empty-title">No services yet</p>
      <p class="empty-sub">Add your first service to start accepting bookings.</p>
      <router-link :to="{ name: 'createService' }" class="create-btn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Create Service
      </router-link>
    </div>

    <!-- Cards -->
    <div v-else class="cards">
      <div
        v-for="service in serviceStore.services"
        :key="service.id"
        class="card"
        :class="{ 'is-editing': editingId === service.id }"
      >

        <!-- VIEW MODE -->
        <template v-if="editingId !== service.id">

          <div class="card-banner">
            <template v-if="service.images?.length">
              <img
                :src="imgUrl(service.images[0].image_url)"
                class="banner-img"
                style="cursor: zoom-in;"
                @click="openGallery(service.images, 0)"
              />
              <div
                v-if="service.images.length > 1"
                class="banner-peek"
                @click="openGallery(service.images, 1)"
              >
                <img :src="imgUrl(service.images[1].image_url)" class="peek-img" />
                <div v-if="service.images.length > 2" class="peek-more">
                  +{{ service.images.length - 2 }}
                </div>
              </div>
            </template>
            <div v-else class="banner-placeholder">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
          </div>

          <div class="card-body">
            <div class="svc-name">{{ service.name }}</div>
            <div class="svc-desc">{{ service.description }}</div>
            <div class="meta-row">
              <span class="pill pill-price">₱{{ service.price.toLocaleString() }}</span>
              <span class="pill pill-dur">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
                {{ service.duration_minutes }} min
              </span>
            </div>
          </div>

          <div class="card-footer">
            <button class="btn btn-edit" @click="startEdit(service)">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4z"/>
              </svg>
              Edit
            </button>

            <template v-if="deleteConfirmId === service.id">
              <span class="delete-confirm-label">Delete this?</span>
              <button class="btn btn-confirm-yes" @click="deleteService(service.id)">Yes</button>
              <button class="btn btn-confirm-no" @click="deleteConfirmId = null">No</button>
            </template>
            <button v-else class="btn btn-del" @click="deleteConfirmId = service.id">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                <path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
              </svg>
              Delete
            </button>
          </div>

        </template>

        <!-- EDIT MODE -->
        <template v-else>
          <div class="edit-header">
            <span class="edit-label">Editing service</span>
            <button class="icon-btn" @click="cancelEdit">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <div class="edit-form">
            <div class="field">
              <label>Service name</label>
              <input v-model="form.name" class="inp" placeholder="e.g. Deep Tissue Massage" />
            </div>

            <div class="field">
              <label>Description</label>
              <textarea v-model="form.description" class="inp inp-textarea" placeholder="Describe what's included..." rows="2" />
            </div>

            <div class="field-row">
              <div class="field">
                <label>Price (₱)</label>
                <div class="inp-prefix-wrap">
                  <span class="inp-prefix">₱</span>
                  <input v-model.number="form.price" class="inp inp-prefixed" type="number" placeholder="0" />
                </div>
              </div>
              <div class="field">
                <label>Duration</label>
                <div class="inp-suffix-wrap">
                  <input v-model.number="form.duration_minutes" class="inp inp-suffixed" type="number" placeholder="60" />
                  <span class="inp-suffix">min</span>
                </div>
              </div>
            </div>

            <div class="field">
              <label>Photos</label>
              <div class="photo-grid">
                <div v-for="img in getService(editingId!)?.images ?? []" :key="img.id" class="ph-thumb">
                  <img :src="imgUrl(img.image_url)" class="ph-img" alt="" />
                  <button class="ph-rm" @click="removeExistingImage(editingId!, img.id)">✕</button>
                </div>
                <div v-for="(src, i) in imagePreviews" :key="'new-' + i" class="ph-thumb">
                  <img :src="src" class="ph-img" alt="" />
                  <button class="ph-rm" @click="removePreview(i)">✕</button>
                </div>
                <label class="ph-add">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                  <input type="file" accept="image/*" multiple class="file-input" @change="onImageChange" />
                </label>
              </div>
            </div>

            <div class="edit-actions">
              <button class="btn btn-cancel" @click="cancelEdit">Cancel</button>
              <button class="btn btn-save" @click="saveEdit">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Save changes
              </button>
            </div>
          </div>
        </template>

      </div>
    </div>

    <!-- Bottom spacer for mobile navigation -->
    <div class="bottom-spacer"></div>

    <!-- Gallery Viewer -->
    <Teleport to="body">
      <div v-if="viewingGallery" class="img-viewer-ov" @click.self="closeGallery">
        <button class="close-viewer" @click="closeGallery">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
        <button v-if="galleryImages.length > 1" class="gallery-nav gallery-prev" @click="galleryPrev">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </button>
        <img :src="galleryImages[galleryIndex]" class="gallery-img" />
        <button v-if="galleryImages.length > 1" class="gallery-nav gallery-next" @click="galleryNext">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
        <div v-if="galleryImages.length > 1" class="gallery-dots">
          <button
            v-for="(_, i) in galleryImages"
            :key="i"
            class="gallery-dot"
            :class="{ active: i === galleryIndex }"
            @click="galleryIndex = i"
          />
        </div>
      </div>
    </Teleport>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100%;
  padding: 32px 28px 120px;
}

.bottom-spacer {
  display: none;
  height: 0;
}

@media (max-width: 768px) {
  .page {
    padding-bottom: 300px;
  }
  .bottom-spacer {
    display: block;
    height: 100px;
  }
}


.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  letter-spacing: -0.3px;
}

.service-count {
  font-size: 12px;
  color: rgba(255,255,255,0.35);
}

.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 10px;
  background: #7c3aed;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background 0.15s;
}

.create-btn:hover { background: #6d28d9; }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 64px 20px;
  gap: 8px;
  text-align: center;
}

.empty-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(255,255,255,0.05);
  border: 0.5px solid rgba(255,255,255,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.3);
  margin-bottom: 8px;
}

.empty-title { font-size: 15px; font-weight: 500; color: #fff; }
.empty-sub { font-size: 13px; color: rgba(255,255,255,0.4); margin-bottom: 12px; }

.cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  max-width: 1100px;
}

.card {
  background: rgba(255,255,255,0.04);
  border: 0.5px solid rgba(255,255,255,0.09);
  border-radius: 16px;
  overflow: hidden;
  transition: border-color 0.2s;
  display: flex;
  flex-direction: column;
}

.card:hover { border-color: rgba(255,255,255,0.16); }

.card.is-editing {
  border-color: rgba(124,58,237,0.5);
  background: rgba(124,58,237,0.04);
}

.card-banner {
  height: 120px;
  background: rgba(255,255,255,0.03);
  overflow: hidden;
  flex-shrink: 0;
  display: flex;
  gap: 2px;
}

.banner-img {
  flex: 1;
  min-width: 0;
  height: 100%;
  object-fit: cover;
  display: block;
}

.banner-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.15);
}

.banner-peek {
  position: relative;
  width: 56px;
  flex-shrink: 0;
  cursor: zoom-in;
  overflow: hidden;
}

.peek-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  opacity: 0.85;
  transition: opacity 0.15s;
}

.banner-peek:hover .peek-img { opacity: 1; }

.peek-more {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.52);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
}

.card-body {
  padding: 14px 16px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.svc-name { font-size: 14px; font-weight: 600; color: #fff; }

.svc-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.45);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta-row { display: flex; gap: 6px; flex-wrap: wrap; }

.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 999px;
}

.pill-price { background: rgba(124,58,237,0.2); color: #c4b5fd; }
.pill-dur { background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.5); border: 0.5px solid rgba(255,255,255,0.08); }

.card-footer {
  padding: 10px 14px 14px;
  border-top: 0.5px solid rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.delete-confirm-label { font-size: 12px; color: rgba(255,255,255,0.5); }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 0.5px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.7);
  transition: background 0.12s, color 0.12s, border-color 0.12s;
  font-family: inherit;
}

.btn:hover { background: rgba(255,255,255,0.09); color: #fff; }
.btn-edit:hover { border-color: rgba(124,58,237,0.4); color: #c4b5fd; }

.btn-del { color: rgba(248,113,113,0.7); border-color: transparent; background: transparent; }
.btn-del:hover { background: rgba(248,113,113,0.1); color: #f87171; border-color: rgba(248,113,113,0.2); }

.btn-confirm-yes { background: rgba(220,38,38,0.15); color: #f87171; border-color: rgba(220,38,38,0.2); }
.btn-confirm-yes:hover { background: rgba(220,38,38,0.25); color: #fca5a5; }

.btn-confirm-no { background: transparent; border-color: rgba(255,255,255,0.08); color: rgba(255,255,255,0.4); }

.btn-save { background: #7c3aed; color: #fff; border-color: transparent; }
.btn-save:hover { background: #6d28d9; color: #fff; }

.btn-cancel { background: transparent; border-color: rgba(255,255,255,0.08); color: rgba(255,255,255,0.4); }
.btn-cancel:hover { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.7); }

.icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  border: 0.5px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.12s;
}

.icon-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }

.edit-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 0.5px solid rgba(124,58,237,0.2);
  background: rgba(124,58,237,0.06);
}

.edit-label {
  font-size: 11px;
  font-weight: 500;
  color: #a78bfa;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.edit-form { padding: 16px; display: flex; flex-direction: column; gap: 14px; }

.field { display: flex; flex-direction: column; gap: 6px; }

.field label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.inp {
  width: 100%;
  padding: 9px 11px;
  border-radius: 9px;
  border: 0.5px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.05);
  color: #fff;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.inp::placeholder { color: rgba(255,255,255,0.2); }

.inp:focus {
  border-color: rgba(124,58,237,0.6);
  box-shadow: 0 0 0 3px rgba(124,58,237,0.12);
}

.inp-textarea { resize: vertical; min-height: 60px; }

.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

.inp-prefix-wrap,
.inp-suffix-wrap { position: relative; display: flex; align-items: center; }

.inp-prefix { position: absolute; left: 11px; font-size: 13px; color: rgba(255,255,255,0.35); pointer-events: none; }
.inp-suffix { position: absolute; right: 11px; font-size: 12px; color: rgba(255,255,255,0.35); pointer-events: none; }
.inp-prefixed { padding-left: 22px; }
.inp-suffixed { padding-right: 36px; }

.photo-grid { display: flex; flex-wrap: wrap; gap: 8px; }

.ph-thumb { position: relative; width: 58px; height: 58px; flex-shrink: 0; }

.ph-img {
  width: 58px;
  height: 58px;
  object-fit: cover;
  border-radius: 9px;
  border: 0.5px solid rgba(255,255,255,0.1);
  display: block;
}

.ph-rm {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ef4444;
  color: #fff;
  border: none;
  cursor: pointer;
  font-size: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: background 0.12s;
}

.ph-rm:hover { background: #dc2626; }

.ph-add {
  width: 58px;
  height: 58px;
  border-radius: 9px;
  border: 0.5px dashed rgba(255,255,255,0.2);
  background: rgba(255,255,255,0.03);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: rgba(255,255,255,0.25);
  transition: border-color 0.12s, color 0.12s;
}

.ph-add:hover { border-color: rgba(124,58,237,0.5); color: #a78bfa; }

.file-input { display: none; }

.edit-actions { display: flex; justify-content: flex-end; gap: 8px; padding-top: 4px; }

.state-msg {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.4);
  font-size: 14px;
  padding: 40px 0;
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 0.9s linear infinite; }

.img-viewer-ov {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.92);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: zoom-out;
}

.gallery-img {
  max-width: 90vw;
  max-height: 85vh;
  border-radius: 12px;
  object-fit: contain;
  display: block;
  cursor: default;
}

.close-viewer {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: 0.5px solid rgba(255,255,255,0.2);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.12s;
}

.close-viewer:hover { background: rgba(255,255,255,0.2); }

.gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  border: 0.5px solid rgba(255,255,255,0.2);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.12s;
  z-index: 1;
}

.gallery-nav:hover { background: rgba(255,255,255,0.2); }
.gallery-prev { left: 20px; }
.gallery-next { right: 20px; }

.gallery-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
}

.gallery-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.3);
  cursor: pointer;
  padding: 0;
  transition: background 0.15s, transform 0.15s;
}

.gallery-dot.active { background: #fff; transform: scale(1.3); }

@media (max-width: 860px) {
  .cards { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .page { padding: 20px 16px 140px; }
}
</style>