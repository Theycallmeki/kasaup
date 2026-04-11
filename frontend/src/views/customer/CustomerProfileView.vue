<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useAuthStore } from "../../stores/authStore"
import LocationPickerMap from "../../components/LocationPickerMap.vue"
import api from "../../services/api"
import { useNotification } from "../../hooks/useNotification"
import { useLoading } from "../../hooks/useLoading"

const auth = useAuthStore()
const { notifySuccess, notifyError } = useNotification()
const { startLoading, stopLoading } = useLoading()
const loading = ref(false)
const message = ref({ text: "", type: "" })

const form = ref({
  full_name: "",
  email: "",
  phone: "",
  address: "",
  latitude: null as number | null,
  longitude: null as number | null
})

const profileImageUrl = ref<string | null>(null)
const uploadingImage = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

onMounted(async () => {
  startLoading("Loading your profile...")
  try {
    if (!auth.user) await auth.fetchUser()
    if (auth.user) {
      form.value.full_name = auth.user.full_name || ""
      form.value.email = auth.user.email || ""
      form.value.phone = auth.user.phone || ""
      form.value.address = auth.user.address || ""
      form.value.latitude = auth.user.latitude || null
      form.value.longitude = auth.user.longitude || null
      profileImageUrl.value = auth.user.profile_image || null
    }
  } finally {
    stopLoading()
  }
})

const onLocationSelected = (loc: { latitude: number; longitude: number }) => {
  form.value.latitude = loc.latitude
  form.value.longitude = loc.longitude
}

const saveProfile = async () => {
  startLoading("Updating your profile...")
  loading.value = true
  message.value = { text: "", type: "" }
  try {
    const res = await api.put("/users/me", form.value)
    auth.user = res.data
    notifySuccess("Success", "Profile updated successfully!")
    message.value = { text: "Profile updated successfully!", type: "success" }
  } catch (err: any) {
    const errorText = err.response?.data?.detail || "Failed to update profile."
    notifyError("Error", errorText)
    message.value = { 
      text: errorText, 
      type: "error" 
    }
  } finally {
    loading.value = false
    stopLoading()
  }
}

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleImageUpload = async (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  startLoading("Uploading your photo...")
  uploadingImage.value = true
  const formData = new FormData()
  formData.append("file", file)

  try {
    const res = await api.post("/users/me/profile-image/", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    })
    profileImageUrl.value = res.data.url
    if (auth.user) {
      auth.user.profile_image = res.data.url
    }
    message.value = { text: "Profile picture updated!", type: "success" }
  } catch (err: any) {
    message.value = {
      text: err.response?.data?.detail || "Failed to upload image.",
      type: "error"
    }
  } finally {
    uploadingImage.value = false
    stopLoading()
  }
}

const displayImageUrl = computed(() => {
  const path = profileImageUrl.value;
  if (!path || path === 'null' || path.trim() === '') return null;
  if (path.startsWith("http") || path.startsWith("data:")) return path;
  
  const base = api.defaults.baseURL?.replace(/\/$/, '') || '';
  const safePath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${safePath}`;
})
</script>

<template>
  <div class="profile-page">
    <div class="header">
      <h1 class="title">My Profile</h1>
      <p class="subtitle">Manage your account details and service location.</p>
    </div>

    <div class="profile-grid">
      <!-- Left: Avatar + Form -->
      <div class="profile-card info-section">
        <!-- Avatar Upload -->
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerUpload">
            <img v-if="displayImageUrl" :src="displayImageUrl" alt="Profile" class="avatar-img" />
            <div v-else class="avatar-placeholder">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </div>
            <div class="avatar-overlay" :class="{ uploading: uploadingImage }">
              <svg v-if="!uploadingImage" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                <circle cx="12" cy="13" r="4"/>
              </svg>
              <span v-else class="spin" />
            </div>
          </div>
          <input 
            ref="fileInput" 
            type="file" 
            accept="image/*" 
            class="hidden-input" 
            @change="handleImageUpload"
          />
          <p class="avatar-hint">Click to change photo</p>
        </div>

        <h2 class="section-title">Personal Settings</h2>
        
        <form @submit.prevent="saveProfile" class="form-stack">
          <div class="input-group">
            <label>Full Name</label>
            <input v-model="form.full_name" type="text" placeholder="Your Name" />
          </div>

          <div class="input-group">
            <label>Email Address</label>
            <input v-model="form.email" type="email" placeholder="email@example.com" />
          </div>

          <div class="input-group">
            <label>Phone Number</label>
            <input v-model="form.phone" type="tel" placeholder="0917XXXXXXX" />
          </div>

          <div class="input-group">
            <label>Street Address</label>
            <input v-model="form.address" type="text" placeholder="House No., Street, Brgy, City" />
          </div>

          <div v-if="message.text" :class="['alert', message.type]">
            {{ message.text }}
          </div>

          <button type="submit" class="save-btn" :disabled="loading">
            <span v-if="loading" class="spin" />
            {{ loading ? 'Saving Changes...' : 'Update Profile' }}
          </button>
        </form>
      </div>

      <!-- Right: Location -->
      <div class="profile-card location-section">
        <div class="loc-head">
           <h2 class="section-title">Service Location</h2>
           <p class="loc-desc">This is used to calculate distance to nearby services.</p>
        </div>
        
        <div class="map-container">
          <LocationPickerMap @location-selected="onLocationSelected" />
        </div>

        <div class="loc-status" v-if="form.latitude">
          <div class="status-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            Location Pin Set
          </div>
          <span class="coord-text">{{ form.latitude.toFixed(5) }}, {{ form.longitude?.toFixed(5) }}</span>
        </div>
        <div class="loc-status warning" v-else>
           <div class="status-badge">!</div>
           Location not set. You won't be able to filter by distance.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="../../styles/customer/CustomerProfileView.css"></style>
