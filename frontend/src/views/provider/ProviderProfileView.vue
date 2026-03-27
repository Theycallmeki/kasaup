<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useProviderStore } from "../../stores/providerStore"

const providerStore = useProviderStore()

const shop_name = ref("")
const description = ref("")
const phone = ref("")
const email = ref("")
const address = ref("")
const offers_home_service = ref(false)

const loading = ref(false)
const saved = ref(false)

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

const save = async () => {
  loading.value = true
  saved.value = false

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