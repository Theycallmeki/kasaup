<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { createProvider, uploadProviderImage, getMyProvider } from "../../services/providers"
import LocationPickerMap from "../../components/LocationPickerMap.vue"
import { useNotification } from "../../hooks/useNotification"
import { useAuthStore } from "../../stores/authStore"

const router = useRouter()
const auth = useAuthStore()
const { notifySuccess, notifyError } = useNotification()

onMounted(async () => {
  try {
    const existingProvider = await getMyProvider()
    if (existingProvider) {
      router.push("/provider/dashboard")
    }
  } catch (err) {
    // No existing provider, stay on this page
  }
})

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")

const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

const offers_home_service = ref(false)

const profileImageFile = ref<File | null>(null)
const profileImagePreview = ref<string | null>(null)

const loading = ref(false)
const error = ref("")

function setLocation(data: any) {
  latitude.value = data.latitude
  longitude.value = data.longitude
}

function onImageChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  profileImageFile.value = file
  profileImagePreview.value = URL.createObjectURL(file)
}

const create = async () => {
  error.value = ""
  loading.value = true

  try {
    if (!shop_name.value.trim()) { error.value = "Shop name is required"; loading.value = false; return }
    if (!phone.value.trim())     { error.value = "Phone is required";     loading.value = false; return }
    if (!email.value.trim())     { error.value = "Email is required";     loading.value = false; return }
    if (latitude.value === null || longitude.value === null) {
      error.value = "Please select your shop location on the map"
      loading.value = false
      return
    }

    const provider = await createProvider({
      shop_name: shop_name.value,
      description: description.value,
      phone: phone.value,
      email: email.value,
      address: address.value,
      latitude: latitude.value,
      longitude: longitude.value,
      offers_home_service: offers_home_service.value
    })

    if (profileImageFile.value) {
      await uploadProviderImage(provider.id, profileImageFile.value)
    }

    // Refresh the user so the router knows we have a profile!
    await auth.fetchUser()

    notifySuccess("Success", "Provider profile created successfully!")
    router.push("/provider/dashboard")
  } catch (err: any) {
    const msg = err.response?.data?.detail || "Failed to create provider"
    notifyError("Error", msg)
    error.value = msg
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <p class="eyebrow">Provider Setup</p>
      <h1 class="title">Create Provider Profile</h1>
      <p class="subtitle">Set up your shop details and pin your location on the map.</p>
    </div>

    <div class="layout">

      <!-- Left: Form -->
      <div class="form-col">

        <!-- Profile Image -->
        <div class="section-card">
          <h2 class="section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
            Profile Image
          </h2>
          <div class="image-upload-wrap">
            <div class="image-preview" :class="{ 'has-image': profileImagePreview }">
              <img v-if="profileImagePreview" :src="profileImagePreview" alt="Profile preview" />
              <div v-else class="image-placeholder">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
                </svg>
                <span>No image selected</span>
              </div>
            </div>
            <label class="image-btn" for="profile-image-input">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              {{ profileImageFile ? "Change Image" : "Upload Image" }}
            </label>
            <input id="profile-image-input" type="file" accept="image/*" class="hidden-input" @change="onImageChange" />
          </div>
        </div>

        <!-- Shop Details -->
        <div class="section-card">
          <h2 class="section-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
            Shop Details
          </h2>

          <div class="field-row">
            <div class="field">
              <label for="shop-name">Shop Name</label>
              <input id="shop-name" v-model="shop_name" class="input" placeholder="e.g. Juan's Plumbing" />
            </div>
            <div class="field">
              <label for="shop-phone">Phone</label>
              <input id="shop-phone" v-model="phone" class="input" placeholder="+63 9XX XXX XXXX" />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label for="shop-email">Email</label>
              <input id="shop-email" v-model="email" class="input" type="email" placeholder="you@example.com" />
            </div>
            <div class="field">
              <label for="shop-address">Address</label>
              <input id="shop-address" v-model="address" class="input" placeholder="Street, City" />
            </div>
          </div>

          <div class="field">
            <label for="shop-desc">Description</label>
            <textarea id="shop-desc" v-model="description" class="input" placeholder="Tell customers what you offer..." />
          </div>
        </div>

        <!-- Home Service Toggle -->
        <label class="checkbox-row">
          <div class="checkbox-wrap">
            <input type="checkbox" v-model="offers_home_service" class="checkbox-input" />
            <div class="checkbox-box">
              <svg v-if="offers_home_service" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </div>
          </div>
          <div>
            <span class="checkbox-label">Offers Home Service</span>
            <p class="checkbox-hint">You travel to the customer's location</p>
          </div>
        </label>

        <!-- Error -->
        <p v-if="error" class="error-msg">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ error }}
        </p>

        <!-- Submit -->
        <button class="submit-btn" :disabled="loading" @click="create">
          <svg v-if="!loading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
            <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
          </svg>
          {{ loading ? "Creating..." : "Create Provider Profile" }}
        </button>

      </div>

      <!-- Right: Map Card -->
      <div class="map-col">
        <div class="map-card">
          <div class="map-card-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="map-pin-icon">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            <div>
              <h3 class="map-card-title">Shop Location</h3>
              <p class="map-card-desc">Click or drag the pin to set your exact shop location.</p>
            </div>
          </div>

          <div class="map-wrap">
            <LocationPickerMap @location-selected="setLocation" />
          </div>

          <div v-if="latitude && longitude" class="coords-row">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
            </svg>
            <span>{{ latitude.toFixed(5) }}, {{ longitude.toFixed(5) }}</span>
          </div>
          <div v-else class="coords-hint-empty">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            No location pinned yet
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px 60px;
  font-family: 'DM Sans', sans-serif;
  color: #e8e8f0;
}

.page-header { margin-bottom: 32px; }

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #a78bfa;
  margin: 0 0 6px;
  font-weight: 600;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.9rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.35);
  margin: 0;
}

/* Layout */
.layout {
  display: flex;
  align-items: flex-start;
  gap: 28px;
}

.form-col {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.map-col {
  width: 460px;
  flex-shrink: 0;
  position: sticky;
  top: 36px;
  align-self: flex-start;
}

/* Section Cards */
.section-card {
  background: rgba(255, 255, 255, 0.025);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.09em;
  margin: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

label {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s, background 0.15s;
}
.input::placeholder { color: rgba(255, 255, 255, 0.2); }
.input:focus {
  border-color: rgba(167, 139, 250, 0.5);
  background: rgba(167, 139, 250, 0.03);
}

textarea.input {
  resize: vertical;
  min-height: 90px;
}

.image-upload-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
}

.image-preview {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.04);
  overflow: hidden;
  flex-shrink: 0;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: rgba(255, 255, 255, 0.15);
}

.image-placeholder span {
  font-size: 9px;
  text-align: center;
}

.image-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 16px;
  background: rgba(124, 58, 237, 0.12);
  border: 0.5px solid rgba(124, 58, 237, 0.35);
  border-radius: 8px;
  color: rgba(167, 139, 250, 0.9);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
  text-transform: none;
  letter-spacing: normal;
}
.image-btn:hover { background: rgba(124, 58, 237, 0.22); }

.hidden-input { display: none; }

.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 18px;
  background: rgba(255, 255, 255, 0.025);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  text-transform: none;
  letter-spacing: normal;
  transition: border-color 0.2s;
}
.checkbox-row:hover { border-color: rgba(167, 139, 250, 0.25); }

.checkbox-wrap { position: relative; flex-shrink: 0; margin-top: 2px; }
.checkbox-input { position: absolute; opacity: 0; width: 0; height: 0; }
.checkbox-box {
  width: 18px;
  height: 18px;
  border-radius: 5px;
  border: 0.5px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, border-color 0.15s;
  color: #fff;
}
.checkbox-input:checked ~ .checkbox-box {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border-color: transparent;
}
.checkbox-label {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  display: block;
  margin-bottom: 3px;
}
.checkbox-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #f87171;
  background: rgba(248, 113, 113, 0.07);
  border: 0.5px solid rgba(248, 113, 113, 0.2);
  border-radius: 10px;
  padding: 11px 14px;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: none;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s, box-shadow 0.15s;
}
.submit-btn:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
}
.submit-btn:disabled { opacity: 0.45; cursor: not-allowed; }

/* Map Card */
.map-card {
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(167, 139, 250, 0.18);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
  width: 100%;
  box-sizing: border-box;
}

.map-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.map-pin-icon { color: #a78bfa; flex-shrink: 0; margin-top: 2px; }

.map-card-title {
  font-family: 'Sora', sans-serif;
  font-size: 1rem;
  color: #c4b5fd;
  margin: 0 0 4px;
}

.map-card-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.38);
  margin: 0;
  line-height: 1.5;
}

.map-wrap {
  border-radius: 12px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.07);
  height: 420px;
  background: #0e0c1a;
}

.coords-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 14px;
  padding-top: 14px;
  font-size: 12px;
  font-family: ui-monospace, monospace;
  color: #a78bfa;
  border-top: 1px dashed rgba(255, 255, 255, 0.07);
}

.coords-hint-empty {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 14px;
  padding-top: 14px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.22);
  border-top: 1px dashed rgba(255, 255, 255, 0.07);
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; }

@media (max-width: 900px) {
  .layout { flex-direction: column; }
  .map-col { width: 100%; position: static; }
}

@media (max-width: 540px) {
  .page { padding: 24px 16px 48px; }
  .field-row { grid-template-columns: 1fr; }
  .title { font-size: 1.5rem; }
}
</style>