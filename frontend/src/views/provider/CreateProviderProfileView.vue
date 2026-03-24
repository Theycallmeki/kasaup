<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { createProvider, uploadProviderImage } from "../../services/providers"
import LocationPickerMap from "../../components/LocationPickerMap.vue"

const router = useRouter()

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

    router.push("/provider/dashboard")
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to create provider"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1 class="title">Create Provider Profile</h1>

    <div class="form">

      <div class="field">
        <label>Profile Image</label>
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

      <div class="field">
        <label>Shop Location</label>
        <div class="map-wrap">
          <LocationPickerMap @location-selected="setLocation" />
        </div>
        <p v-if="latitude && longitude" class="coords-hint">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
          </svg>
          {{ latitude.toFixed(5) }}, {{ longitude.toFixed(5) }}
        </p>
      </div>

      <p v-if="error" class="error-msg">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ error }}
      </p>

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
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
  max-width: 700px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.01em;
  margin: 0 0 28px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  font-size: 12px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.input {
  width: 100%;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
}
.input::placeholder { color: rgba(255, 255, 255, 0.2); }
.input:focus { border-color: rgba(167, 139, 250, 0.5); }

textarea.input {
  resize: vertical;
  min-height: 90px;
}

.image-upload-wrap {
  display: flex;
  align-items: center;
  gap: 14px;
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
  color: rgba(255, 255, 255, 0.2);
}

.image-placeholder span {
  font-size: 9px;
  text-align: center;
  line-height: 1.2;
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
}
.image-btn:hover {
  background: rgba(124, 58, 237, 0.25);
}

.hidden-input {
  display: none;
}

.checkbox-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  cursor: pointer;
  text-transform: none;
  letter-spacing: normal;
}
.checkbox-wrap {
  position: relative;
  flex-shrink: 0;
  margin-top: 2px;
}
.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
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
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  display: block;
  margin-bottom: 2px;
}
.checkbox-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
}

.map-wrap {
  border-radius: 12px;
  overflow: hidden;
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  height: 280px;
}

.coords-hint {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: rgba(167, 139, 250, 0.7);
  margin-top: 2px;
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  color: #f87171;
  background: rgba(248, 113, 113, 0.08);
  border: 0.5px solid rgba(248, 113, 113, 0.2);
  border-radius: 8px;
  padding: 10px 14px;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 13px;
  border-radius: 12px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: none;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s;
}
.submit-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}
.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin 1s linear infinite; }

@media (max-width: 540px) {
  .page { padding: 24px 16px; }
  .field-row { grid-template-columns: 1fr; }
}
</style>