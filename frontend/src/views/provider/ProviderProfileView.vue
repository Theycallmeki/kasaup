<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useProviderStore } from "../../stores/providerStore"
import api from "../../services/api"

const providerStore = useProviderStore()

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")
const offers_home_service = ref(false)

const loading = ref(false)
const saved = ref(false)

const imageLoading = ref(false)
const imagePreview = ref<string | null>(null)
const pendingImageFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const displayImage = computed(() => {
  if (imagePreview.value) return imagePreview.value
  if (providerStore.myProvider?.profile_image) {
    const path = providerStore.myProvider.profile_image.replace(/^\//, "")
    return `${api.defaults.baseURL}/${path}`
  }
  return null
})

const shopInitials = computed(() => {
  const name = shop_name.value || providerStore.myProvider?.shop_name || ""
  return name.split(" ").map((w: string) => w[0]).join("").slice(0, 2).toUpperCase()
})

onMounted(async () => {
  await providerStore.fetchMyProvider()

  if (providerStore.myProvider) {
    const p = providerStore.myProvider
    shop_name.value = p.shop_name
    description.value = p.description
    phone.value = p.phone
    email.value = p.email
    address.value = p.address
    offers_home_service.value = p.offers_home_service
  }
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  pendingImageFile.value = file

  const reader = new FileReader()
  reader.onload = (ev) => {
    imagePreview.value = ev.target?.result as string
  }
  reader.readAsDataURL(file)

  if (fileInput.value) fileInput.value.value = ""
}

const save = async () => {
  loading.value = true
  saved.value = false

  if (pendingImageFile.value) {
    const providerId = providerStore.myProvider?.id
    if (providerId) {
      await providerStore.uploadProfileImage(providerId, pendingImageFile.value)
      pendingImageFile.value = null
      imagePreview.value = null
    }
  }

  await providerStore.updateMy({
    shop_name: shop_name.value,
    description: description.value,
    phone: phone.value,
    email: email.value,
    address: address.value,
    offers_home_service: offers_home_service.value
  })

  loading.value = false
  saved.value = true
  setTimeout(() => (saved.value = false), 2500)
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">My Profile</h1>
      <p class="hint">Update your shop details visible to customers.</p>
    </div>

    <div class="form-card">

      <!-- Profile Picture -->
      <div class="avatar-section">
        <div class="avatar-wrapper" @click="triggerFileInput">
          <img v-if="displayImage" :src="displayImage" class="avatar-img" alt="Profile" />
          <div v-else class="avatar-placeholder">
            <span class="avatar-initials">{{ shopInitials || "?" }}</span>
          </div>

          <div class="avatar-overlay" :class="{ uploading: imageLoading }">
            <svg v-if="!imageLoading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
              <path d="M21 12a9 9 0 1 1-6.219-8.56" />
            </svg>
          </div>
        </div>

        <div class="avatar-info">
          <span class="avatar-label">Profile Photo</span>
          <button class="avatar-change-btn" @click="triggerFileInput" :disabled="imageLoading">
            {{ imageLoading ? "Uploading..." : "Change photo" }}
          </button>
          <span class="avatar-hint">JPG or PNG, max 5MB</span>
        </div>

        <input
          ref="fileInput"
          type="file"
          accept="image/jpeg,image/png"
          style="display: none"
          @change="onFileChange"
        />
      </div>

      <div class="card-divider" />

      <div class="field-group">
        <label class="field-label">Shop Name</label>
        <input v-model="shop_name" class="field" placeholder="e.g. Maria's Salon" />
      </div>

      <div class="field-row">
        <div class="field-group">
          <label class="field-label">Phone</label>
          <input v-model="phone" class="field" placeholder="+63 912 345 6789" />
        </div>
        <div class="field-group">
          <label class="field-label">Email</label>
          <input v-model="email" class="field" placeholder="shop@email.com" />
        </div>
      </div>

      <div class="field-group">
        <label class="field-label">Address</label>
        <input v-model="address" class="field" placeholder="Street, City, Province" />
      </div>

      <div class="field-group">
        <label class="field-label">Description</label>
        <textarea v-model="description" class="field textarea" placeholder="Tell customers what your shop offers..." />
      </div>

      <div class="card-divider" />

      <label class="checkbox-row">
        <div class="checkbox-box" :class="{ checked: offers_home_service }" @click="offers_home_service = !offers_home_service">
          <svg v-if="offers_home_service" width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="2 6 5 9 10 3" />
          </svg>
        </div>
        <span class="checkbox-label">Offers Home Service</span>
      </label>

      <button class="save-btn" @click="save" :disabled="loading">
        <svg v-if="loading" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
          <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
        <svg v-else-if="saved" width="14" height="14" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="2 6 5 9 10 3" />
        </svg>
        {{ loading ? "Saving..." : saved ? "Saved!" : "Save Changes" }}
      </button>

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
  padding: 24px;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Avatar */
.avatar-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-wrapper {
  position: relative;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  cursor: pointer;
  flex-shrink: 0;
}

.avatar-img {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
}

.avatar-placeholder {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(124, 58, 237, 0.2);
  border: 0.5px solid rgba(124, 58, 237, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-initials {
  font-family: 'Sora', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: rgba(167, 139, 250, 0.9);
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity 0.15s;
}

.avatar-wrapper:hover .avatar-overlay,
.avatar-overlay.uploading {
  opacity: 1;
}

.avatar-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.avatar-label {
  font-size: 12px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.avatar-change-btn {
  font-size: 13px;
  font-weight: 500;
  color: rgba(167, 139, 250, 0.85);
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  text-align: left;
  transition: color 0.15s;
}

.avatar-change-btn:hover:not(:disabled) {
  color: rgba(167, 139, 250, 1);
}

.avatar-change-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.avatar-hint {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.2);
}

/* Fields */
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
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.05em;
  text-transform: uppercase;
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
  width: 100%;
  box-sizing: border-box;
  color-scheme: dark;
}

.field::placeholder {
  color: rgba(255, 255, 255, 0.2);
}

.field:focus {
  border-color: rgba(167, 139, 250, 0.5);
}

.textarea {
  resize: vertical;
  min-height: 90px;
}

.card-divider {
  height: 0.5px;
  background: rgba(255, 255, 255, 0.07);
  margin: 0;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.checkbox-box {
  width: 18px;
  height: 18px;
  border-radius: 5px;
  border: 0.5px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.15s, border-color 0.15s;
}

.checkbox-box.checked {
  background: rgba(124, 58, 237, 0.4);
  border-color: rgba(124, 58, 237, 0.6);
  color: #fff;
}

.checkbox-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
}

.save-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 10px;
  background: rgba(124, 58, 237, 0.35);
  border: 0.5px solid rgba(124, 58, 237, 0.5);
  color: #fff;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  align-self: flex-start;
  transition: background 0.15s;
}

.save-btn:hover:not(:disabled) {
  background: rgba(124, 58, 237, 0.5);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 1s linear infinite;
}

@media (max-width: 640px) {
  .page {
    padding: 24px 16px;
  }

  .field-row {
    flex-direction: column;
  }
}
</style>