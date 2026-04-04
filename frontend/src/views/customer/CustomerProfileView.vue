<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useAuthStore } from "../../stores/authStore"
import LocationPickerMap from "../../components/LocationPickerMap.vue"
import api from "../../services/api"

const auth = useAuthStore()
const loading = ref(false)
const message = ref({ text: "", type: "" })

const form = ref({
  full_name: "",
  email: "",
  phone: "",
  latitude: null as number | null,
  longitude: null as number | null
})

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  if (auth.user) {
    form.value.full_name = auth.user.full_name || ""
    form.value.email = auth.user.email || ""
    form.value.phone = auth.user.phone || ""
    form.value.latitude = auth.user.latitude || null
    form.value.longitude = auth.user.longitude || null
  }
})

const onLocationSelected = (loc: { latitude: number; longitude: number }) => {
  form.value.latitude = loc.latitude
  form.value.longitude = loc.longitude
}

const saveProfile = async () => {
  loading.value = true
  message.value = { text: "", type: "" }
  try {
    const res = await api.put("/users/me", form.value)
    auth.user = res.data
    message.value = { text: "Profile updated successfully!", type: "success" }
  } catch (err: any) {
    message.value = { 
      text: err.response?.data?.detail || "Failed to update profile.", 
      type: "error" 
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <div class="header">
      <h1 class="title">My Profile</h1>
      <p class="subtitle">Manage your account details and service location.</p>
    </div>

    <div class="profile-grid">
      <!-- Left: Form -->
      <div class="profile-card info-section">
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
