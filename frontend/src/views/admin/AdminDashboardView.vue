<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

function goUsers() {
  router.push("/admin/users")
}

function goProviders() {
  router.push("/admin/providers")
}

function goCategories() {
  router.push("/admin/categories")
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <div class="header-label">Admin</div>
      <h1 class="title">Dashboard</h1>
      <p class="hint">Manage platform users, providers, and categories.</p>
    </div>

    <div class="cards">

      <div class="card" @click="goUsers">
        <div class="card-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div class="card-body">
          <h3 class="card-title">Users</h3>
          <p class="card-desc">View and manage registered users</p>
        </div>
        <div class="card-arrow">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>

      <div class="card" @click="goProviders">
        <div class="card-icon card-icon--teal">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
        </div>
        <div class="card-body">
          <h3 class="card-title">Providers</h3>
          <p class="card-desc">Verify and manage service providers</p>
        </div>
        <div class="card-arrow">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>

      <div class="card" @click="goCategories">
        <div class="card-icon card-icon--pink">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
        </div>
        <div class="card-body">
          <h3 class="card-title">Categories</h3>
          <p class="card-desc">Manage service categories</p>
        </div>
        <div class="card-arrow">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped src="@/styles/admin/AdminDashboardView.css"></style>