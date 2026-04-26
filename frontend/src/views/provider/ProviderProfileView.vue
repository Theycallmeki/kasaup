<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useProviderStore } from "../../stores/providerStore"
import { useLoading } from "../../hooks/useLoading"
import { useNotification } from "../../hooks/useNotification"
import api from "../../services/api"
import {
  validateEmail,
  validatePHPhone,
  validateShopName,
  normalizePHPhone
} from "../../utils/validators"

const providerStore = useProviderStore()
const { startLoading, stopLoading } = useLoading()
const { notifySuccess, notifyError } = useNotification()

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")
const offers_home_service = ref(false)

const loading = ref(false)
const saved = ref(false)
const fieldErrors = ref({ shop_name: "", phone: "" })

const imageLoading = ref(false)
const imagePreview = ref<string | null>(null)
const pendingImageFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const displayImage = computed(() => {
  if (imagePreview.value) return imagePreview.value
  const profileImage = providerStore.myProvider?.profile_image
  if (profileImage) {
    if (profileImage.startsWith("http")) return profileImage
    const path = profileImage.replace(/^\//, "")
    return `${api.defaults.baseURL}/${path}`
  }
  return null
})

const shopInitials = computed(() => {
  const name = shop_name.value || providerStore.myProvider?.shop_name || ""
  return name.split(" ").map((w: string) => w[0]).join("").slice(0, 2).toUpperCase()
})

onMounted(async () => {
  startLoading("Fetching profile...")
  try {
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
  } finally {
    stopLoading()
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

const onPhoneBlur = () => {
  const normalized = normalizePHPhone(phone.value)
  if (normalized) phone.value = normalized
  fieldErrors.value.phone = validatePHPhone(phone.value) || ""
}

const validateAll = (): boolean => {
  fieldErrors.value.shop_name = validateShopName(shop_name.value) || ""
  fieldErrors.value.phone = validatePHPhone(phone.value) || ""
  return !Object.values(fieldErrors.value).some(Boolean)
}

const save = async () => {
  if (!validateAll()) return

  startLoading("Updating profile...")
  loading.value = true
  saved.value = false

  try {
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
      address: address.value,
      offers_home_service: offers_home_service.value
    })

    notifySuccess("Saved", "Profile updated successfully!")
    saved.value = true
    setTimeout(() => (saved.value = false), 2500)
  } catch (err: any) {
    const msg = err.response?.data?.detail || "Failed to update profile."
    notifyError("Error", msg)
  } finally {
    loading.value = false
    stopLoading()
  }
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <h1 class="title">My Profile</h1>
      <p class="hint">Update your shop details visible to customers.</p>
    </div>

    <div class="form-card">

      
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
        <input
          v-model="shop_name"
          class="field"
          :class="{ 'field-invalid': fieldErrors.shop_name }"
          placeholder="e.g. Maria's Salon"
          @blur="fieldErrors.shop_name = validateShopName(shop_name) || ''"
        />
        <span v-if="fieldErrors.shop_name" class="field-err">{{ fieldErrors.shop_name }}</span>
      </div>

      <div class="field-row">
        <div class="field-group">
          <label class="field-label">Phone</label>
          <input
            v-model="phone"
            class="field"
            :class="{ 'field-invalid': fieldErrors.phone }"
            placeholder="+63 912 345 6789"
            @blur="onPhoneBlur"
          />
          <span v-if="fieldErrors.phone" class="field-err">{{ fieldErrors.phone }}</span>
        </div>
        <div class="field-group">
          <label class="field-label">Email</label>
          <input
            v-model="email"
            class="field field-readonly"
            readonly
            placeholder="shop@email.com"
          />
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

<style src="../../styles/provider/ProviderProfileView.css" scoped></style>