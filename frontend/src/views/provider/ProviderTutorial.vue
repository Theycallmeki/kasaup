<script setup lang="ts">
import { ref } from 'vue'
import { useScroll } from "../../hooks/useScroll"

const { scrollRef: pageScroll } = useScroll()

const modules = [
  {
    title: "Complete Your Profile",
    desc: "A detailed profile builds trust. Add a clear shop name, description, and profile image.",
    icon: "user"
  },
  {
    title: "List Your Services",
    desc: "Define what you offer, set your prices, and specify the duration for each service.",
    icon: "wrench"
  },
  {
    title: "Set Availability",
    desc: "Configure your working hours so customers can only book when you're available.",
    icon: "clock"
  },
  {
    title: "Manage Appointments",
    desc: "Track incoming requests, view your schedule, and update appointment statuses.",
    icon: "calendar"
  }
]
</script>

<template>
  <div class="page tutorial-page" ref="pageScroll">
    <header class="section-header">
      <div class="eyebrow">Provider Guide</div>
      <h1 class="title">Growing with Kasa<span class="accent">Up</span></h1>
      <p class="subtitle">Learn how to manage your business efficiently and reach more local customers.</p>
    </header>

    <div class="modules-grid">
      <div v-for="(mod, index) in modules" :key="index" class="module-card">
        <div class="module-icon">
          <div class="icon-circle">
            {{ index + 1 }}
          </div>
        </div>
        <div class="module-content">
          <h3 class="module-title">{{ mod.title }}</h3>
          <p class="module-desc">{{ mod.desc }}</p>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <router-link to="/provider/dashboard" class="btn-primary">Go to Dashboard</router-link>
    </div>
  </div>
</template>

<style scoped src="../../styles/provider/ProviderTutorial.css"></style>
