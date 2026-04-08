<template>
  <div class="home">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="hero-card">
      <span class="eyebrow">Manpower Services</span>
      <h1 class="title">Kasa<span class="accent">up</span></h1>
      <p class="subtitle">
        Find trusted local services near you  fast, easy, and reliable.
      </p>

      <div class="actions">
        <button class="btn btn-primary" @click="goProviders">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          Browse Providers
        </button>
        <button class="btn btn-outline" @click="goAuth">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          Get Started
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

const goProviders = () => router.push("/providers")
const goAuth = () => router.push("/auth")
</script>

<style scoped src="../../styles/customer/HomeView.css"></style>