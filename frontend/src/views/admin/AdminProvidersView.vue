<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useProviderStore } from "../../stores/providerStore"

const providerStore = useProviderStore()

const showForm = ref(false)

const form = ref({
  shop_name: "",
  description: "",
  phone: "",
  email: "",
  address: "",
  latitude: 0,
  longitude: 0,
  offers_home_service: false
})

const editingId = ref<number | null>(null)

onMounted(() => {
  providerStore.fetchProviders()
})

function openCreate() {
  resetForm()
  showForm.value = true
}

async function submit() {
  if (editingId.value) {
    await providerStore.editProvider(editingId.value, form.value)
  } else {
    await providerStore.addProvider(form.value)
  }
  resetForm()
}

function edit(provider: any) {
  editingId.value = provider.id
  showForm.value = true

  form.value = {
    shop_name: provider.shop_name,
    description: provider.description,
    phone: provider.phone,
    email: provider.email,
    address: provider.address,
    latitude: provider.latitude,
    longitude: provider.longitude,
    offers_home_service: provider.offers_home_service
  }
}

async function remove(id: number) {
  await providerStore.removeProvider(id)
}

function resetForm() {
  editingId.value = null
  showForm.value = false

  form.value = {
    shop_name: "",
    description: "",
    phone: "",
    email: "",
    address: "",
    latitude: 0,
    longitude: 0,
    offers_home_service: false
  }
}
</script>

<template>
  <div class="provider-page">

    <div class="provider-header">
      <div>
        <h2>Providers</h2>
        <p>Manage service providers on the platform</p>
      </div>

      <button class="btn primary" @click="openCreate">
        + Add Provider
      </button>
    </div>

    <!-- ✅ FORM ONLY WHEN ACTIVE -->
    <form v-if="showForm" @submit.prevent="submit" class="provider-form">

      <div class="form-grid">
        <input v-model="form.shop_name" placeholder="Shop Name" class="field" />
        <input v-model="form.description" placeholder="Description" class="field" />
        <input v-model="form.phone" placeholder="Phone" class="field" />
        <input v-model="form.email" placeholder="Email" class="field" />
        <input v-model="form.address" placeholder="Address" class="field full" />
        <input v-model.number="form.latitude" placeholder="Latitude" class="field" />
        <input v-model.number="form.longitude" placeholder="Longitude" class="field" />

        <label class="checkbox">
          <input type="checkbox" v-model="form.offers_home_service" />
          <span>Offers Home Service</span>
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn primary">
          {{ editingId ? "Update Provider" : "Create Provider" }}
        </button>

        <button type="button" class="btn ghost" @click="resetForm">
          Cancel
        </button>
      </div>

    </form>

    <!-- LIST -->
    <div v-if="providerStore.loading" class="empty">
      Loading...
    </div>

    <div v-else class="provider-grid">

      <div
        v-for="provider in providerStore.providers"
        :key="provider.id"
        class="provider-card"
      >
        <div class="card-top">
          <h3>{{ provider.shop_name }}</h3>
          <span class="badge" v-if="provider.offers_home_service">
            Home Service
          </span>
        </div>

        <p class="desc">{{ provider.description }}</p>

        <div class="meta">
          <span>{{ provider.phone }}</span>
          <span>{{ provider.email }}</span>
        </div>

        <div class="actions">
          <button class="icon-btn" @click="edit(provider)">✏️</button>
          <button class="icon-btn danger" @click="remove(provider.id)">🗑</button>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
.provider-page {
  padding: 32px;
  background: #0e0c1a;
  min-height: 100vh;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
}

/* Header */
.provider-header h2 {
  margin: 0;
}

.provider-header p {
  color: rgba(255,255,255,0.4);
  font-size: 13px;
}

/* Form */
.provider-form {
  margin-top: 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 18px;
  backdrop-filter: blur(10px);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.field {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 10px;
  color: #fff;
}

.field:focus {
  border-color: rgba(167,139,250,0.5);
  outline: none;
}

.full {
  grid-column: span 2;
}

/* Checkbox */
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255,255,255,0.6);
}

/* Buttons */
.form-actions {
  margin-top: 14px;
  display: flex;
  gap: 8px;
}

.btn {
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.btn.primary {
  background: rgba(124,58,237,0.4);
  color: #fff;
}

.btn.primary:hover {
  background: rgba(124,58,237,0.6);
}

.btn.ghost {
  background: transparent;
  color: rgba(255,255,255,0.5);
}

/* Grid */
.provider-grid {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

/* Card */
.provider-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: all 0.2s ease;
}

.provider-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Card content */
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-top h3 {
  font-size: 14px;
  margin: 0;
}

.badge {
  font-size: 10px;
  background: rgba(56,189,248,0.2);
  color: #38bdf8;
  padding: 4px 6px;
  border-radius: 6px;
}

/* Description */
.desc {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

/* Meta */
.meta {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* Actions */
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
  margin-top: auto;
}

.icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: transparent;
  color: rgba(255,255,255,0.4);
  cursor: pointer;
}

.icon-btn:hover {
  background: rgba(167,139,250,0.15);
  color: #a78bfa;
}

.icon-btn.danger:hover {
  background: rgba(248,113,113,0.15);
  color: #f87171;
}

/* Empty */
.empty {
  margin-top: 20px;
  color: rgba(255,255,255,0.4);
}
</style>