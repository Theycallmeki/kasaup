<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { createProvider, uploadProviderImage, getMyProvider } from "../../services/providers"
import LocationPickerMap from "../../components/LocationPickerMap.vue"
import { useNotification } from "../../hooks/useNotification"
import { useAuthStore } from "../../stores/authStore"
import { useLoading } from "../../hooks/useLoading"
import {
  validateEmail,
  validatePHPhone,
  validateShopName,
  normalizePHPhone
} from "../../utils/validators"

const router = useRouter()
const auth = useAuthStore()
const { notifySuccess, notifyError } = useNotification()
const { startLoading, stopLoading } = useLoading()

onMounted(async () => {
  startLoading("Verifying your account...")
  try {
    const existingProvider = await getMyProvider()
    if (existingProvider) {
      router.push("/provider/dashboard")
    }
  } catch (err) {
  
  } finally {
    stopLoading()
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

// Per-field errors
const fieldErrors = ref({ shop_name: "", phone: "", email: "" })

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

const onPhoneBlur = () => {
  const normalized = normalizePHPhone(phone.value)
  if (normalized) phone.value = normalized
  fieldErrors.value.phone = validatePHPhone(phone.value) || ""
}

const validateAll = (): boolean => {
  fieldErrors.value.shop_name = validateShopName(shop_name.value) || ""
  fieldErrors.value.phone = validatePHPhone(phone.value) || ""
  fieldErrors.value.email = email.value.trim() ? (validateEmail(email.value) || "") : ""
  return !Object.values(fieldErrors.value).some(Boolean)
}

const create = async () => {
  error.value = ""
  if (!validateAll()) return

  if (latitude.value === null || longitude.value === null) {
    error.value = "Please select your shop location on the map"
    return
  }

  startLoading("Setting up your provider profile...")

  try {
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

    await auth.fetchUser()

    notifySuccess("Success", "Provider profile created successfully!")
    router.push("/provider/dashboard")
  } catch (err: any) {
    const msg = err.response?.data?.detail || "Failed to create provider"
    notifyError("Error", msg)
    error.value = msg
  } finally {
    stopLoading()
  }
}
</script>

<template>
  <div class="page">
    <div class="container">

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
                <input
                  id="shop-name"
                  v-model="shop_name"
                  class="input"
                  :class="{ 'input-error': fieldErrors.shop_name }"
                  placeholder="e.g. Juan's Plumbing"
                  @blur="fieldErrors.shop_name = validateShopName(shop_name) || ''"
                />
                <span v-if="fieldErrors.shop_name" class="inline-error">{{ fieldErrors.shop_name }}</span>
              </div>
              <div class="field">
                <label for="shop-phone">Phone</label>
                <input
                  id="shop-phone"
                  v-model="phone"
                  class="input"
                  :class="{ 'input-error': fieldErrors.phone }"
                  placeholder="+63 9XX XXX XXXX"
                  @blur="onPhoneBlur"
                />
                <span v-if="fieldErrors.phone" class="inline-error">{{ fieldErrors.phone }}</span>
              </div>
            </div>

            <div class="field-row">
              <div class="field">
                <label for="shop-email">Email</label>
                <input
                  id="shop-email"
                  v-model="email"
                  class="input"
                  :class="{ 'input-error': fieldErrors.email }"
                  type="email"
                  placeholder="you@example.com"
                  @blur="fieldErrors.email = email.trim() ? (validateEmail(email) || '') : ''"
                />
                <span v-if="fieldErrors.email" class="inline-error">{{ fieldErrors.email }}</span>
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

        <!-- Submit Section (Now inside layout) -->
        <div class="actions-row">
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

    </div>
  </div>
</template>

<style scoped src="../../styles/provider/CreateProviderProfileView.css"></style>