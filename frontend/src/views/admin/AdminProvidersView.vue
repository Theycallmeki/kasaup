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
  <div class="page">

    <div class="page-header">
      <div>
        <div class="header-label">Admin</div>
        <h1 class="title">Providers</h1>
        <p class="hint">Verify and manage service providers on the platform.</p>
      </div>
      <button class="add-btn" @click="openCreate">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Add Provider
      </button>
    </div>

    <!-- Form -->
    <form v-if="showForm" @submit.prevent="submit" class="provider-form">
      <div class="form-label-row">
        <span class="form-label-tag">{{ editingId ? 'Edit Provider' : 'New Provider' }}</span>
      </div>

      <div class="form-grid">
        <div class="field-group">
          <label class="field-label">Shop Name</label>
          <input v-model="form.shop_name" placeholder="e.g. Juan's Repair Shop" class="field" />
        </div>
        <div class="field-group">
          <label class="field-label">Description</label>
          <input v-model="form.description" placeholder="Short description" class="field" />
        </div>
        <div class="field-group">
          <label class="field-label">Phone</label>
          <input v-model="form.phone" placeholder="+63..." class="field" />
        </div>
        <div class="field-group">
          <label class="field-label">Email</label>
          <input v-model="form.email" placeholder="provider@email.com" class="field" />
        </div>
        <div class="field-group full">
          <label class="field-label">Address</label>
          <input v-model="form.address" placeholder="Full address" class="field" />
        </div>
        <div class="field-group">
          <label class="field-label">Latitude</label>
          <input v-model.number="form.latitude" placeholder="0.000" class="field" />
        </div>
        <div class="field-group">
          <label class="field-label">Longitude</label>
          <input v-model.number="form.longitude" placeholder="0.000" class="field" />
        </div>

        <label class="checkbox full">
          <input type="checkbox" v-model="form.offers_home_service" />
          <span>Offers Home Service</span>
        </label>
      </div>

      <div class="form-actions">
        <button type="submit" class="action-btn action-btn--save">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          {{ editingId ? 'Update Provider' : 'Create Provider' }}
        </button>
        <button type="button" class="action-btn action-btn--cancel" @click="resetForm">
          Cancel
        </button>
      </div>
    </form>

    <!-- Loading -->
    <div v-if="providerStore.loading" class="state-msg">
      <span class="spinner"></span>
      <p>Loading providers...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="!providerStore.providers.length && !showForm" class="state-msg empty">
      <div class="empty-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          <polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
      </div>
      <h3 class="empty-text">No providers yet</h3>
      <p class="empty-sub">Add your first provider to get started.</p>
    </div>

    <!-- Grid -->
    <div v-else class="provider-grid">

      <div
        v-for="provider in providerStore.providers"
        :key="provider.id"
        class="provider-card"
      >
        <div class="card-top">
          <div class="provider-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </div>
          <span class="home-badge" v-if="provider.offers_home_service">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polygon points="3 11 22 2 13 21 11 13 3 11"/>
            </svg>
            Home Service
          </span>
        </div>

        <h3 class="shop-name">{{ provider.shop_name }}</h3>
        <p class="desc">{{ provider.description }}</p>

        <div class="meta">
          <div class="meta-row" v-if="provider.phone">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.18h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.81a16 16 0 0 0 6 6l.94-.94a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 21.69 16z"/>
            </svg>
            {{ provider.phone }}
          </div>
          <div class="meta-row" v-if="provider.email">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            {{ provider.email }}
          </div>
        </div>

        <div class="card-actions">
          <button class="icon-btn" title="Edit" @click="edit(provider)">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            Edit
          </button>
          <button class="icon-btn icon-btn--danger" title="Delete" @click="remove(provider.id)">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
              <path d="M10 11v6"/><path d="M14 11v6"/>
              <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
            </svg>
            Delete
          </button>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped src="../../styles/admin/AdminProvidersView.css"></style>