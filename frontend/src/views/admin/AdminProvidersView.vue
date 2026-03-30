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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
  color: #fff;
}

/* Header */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.header-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(167, 139, 250, 0.6);
  margin-bottom: 6px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  padding: 9px 16px;
  border-radius: 10px;
  background: rgba(124, 58, 237, 0.35);
  border: 0.5px solid rgba(124, 58, 237, 0.5);
  color: #fff;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.add-btn:hover {
  background: rgba(124, 58, 237, 0.5);
  border-color: rgba(124, 58, 237, 0.7);
}

/* Form */
.provider-form {
  margin-bottom: 28px;
  background: rgba(124, 58, 237, 0.05);
  border: 0.5px dashed rgba(167, 139, 250, 0.35);
  border-radius: 16px;
  padding: 20px;
}

.form-label-row {
  margin-bottom: 16px;
}

.form-label-tag {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(167, 139, 250, 0.7);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-group.full {
  grid-column: span 2;
}

.field-label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.field {
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}
.field::placeholder { color: rgba(255, 255, 255, 0.2); }
.field:focus { border-color: rgba(167, 139, 250, 0.5); }

.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
}

.form-actions {
  margin-top: 16px;
  display: flex;
  gap: 8px;
}

/* Action buttons (form) */
.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 9px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 0.5px solid transparent;
  transition: background 0.15s, border-color 0.15s;
}

.action-btn--save {
  background: rgba(124, 58, 237, 0.3);
  border-color: rgba(124, 58, 237, 0.5);
  color: #fff;
}
.action-btn--save:hover {
  background: rgba(124, 58, 237, 0.5);
}

.action-btn--cancel {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.45);
}
.action-btn--cancel:hover {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
}

/* States */
.state-msg {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 14px;
  justify-content: center;
}
.state-msg.empty {
  flex-direction: column;
  background: rgba(255, 255, 255, 0.015);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}
.empty-icon { color: rgba(167, 139, 250, 0.5); }
.empty-text {
  font-family: 'Sora', sans-serif;
  font-size: 1.1rem;
  color: #fff;
  margin: 4px 0 0;
}
.empty-sub { margin: 4px 0 0; font-size: 13px; }

@keyframes spin { to { transform: rotate(360deg); } }
.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #a78bfa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Grid */
.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 14px;
}

/* Card */
.provider-card {
  background: rgba(255, 255, 255, 0.025);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: border-color 0.2s, background 0.2s;
}
.provider-card:hover {
  border-color: rgba(167, 139, 250, 0.25);
  background: rgba(255, 255, 255, 0.035);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.provider-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(99, 60, 220, 0.2);
  border: 0.5px solid rgba(130, 90, 255, 0.3);
  color: #a78bfa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.home-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 10px;
  font-weight: 600;
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 0.5px solid rgba(56, 189, 248, 0.25);
  padding: 3px 8px;
  border-radius: 100px;
  letter-spacing: 0.03em;
}

.shop-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  line-height: 1.5;
  flex: 1;
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 2px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.35);
}
.meta-row svg { color: rgba(167, 139, 250, 0.5); flex-shrink: 0; }

/* Card action buttons */
.card-actions {
  display: flex;
  gap: 6px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 0.5px solid rgba(255, 255, 255, 0.06);
}

.icon-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 7px 10px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 0.5px solid transparent;
  color: rgba(255, 255, 255, 0.45);
  background: rgba(255, 255, 255, 0.04);
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.icon-btn:hover {
  background: rgba(167, 139, 250, 0.12);
  border-color: rgba(167, 139, 250, 0.2);
  color: #a78bfa;
}

.icon-btn--danger {
  color: rgba(248, 113, 113, 0.5);
  background: transparent;
}
.icon-btn--danger:hover {
  background: rgba(248, 113, 113, 0.1);
  border-color: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

@media (max-width: 640px) {
  .page { padding: 24px 16px; }
  .form-grid { grid-template-columns: 1fr; }
  .field-group.full { grid-column: span 1; }
  .provider-grid { grid-template-columns: 1fr; }
}
</style>