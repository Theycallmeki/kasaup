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
    <!-- Background Orbs -->
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

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

<style scoped>
.tutorial-page {
  position: relative;
  min-height: 100%;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  overflow-x: hidden;
  background: #0e0c1a;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  scrollbar-width: thin;
  scrollbar-color: rgba(96, 165, 250, 0.2) transparent;
}

.tutorial-page::-webkit-scrollbar {
  width: 6px;
}
.tutorial-page::-webkit-scrollbar-track {
  background: transparent;
}
.tutorial-page::-webkit-scrollbar-thumb {
  background: rgba(96, 165, 250, 0.2);
  border-radius: 10px;
}
.tutorial-page::-webkit-scrollbar-thumb:hover {
  background: rgba(96, 165, 250, 0.4);
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
  opacity: 0.3;
  z-index: 0;
}
.orb1 {
  width: 450px;
  height: 450px;
  top: -150px;
  right: -200px;
  background: radial-gradient(circle, #3b82f6 0%, transparent 70%);
}
.orb2 {
  width: 350px;
  height: 350px;
  bottom: -50px;
  left: -100px;
  background: radial-gradient(circle, #6366f1 0%, transparent 70%);
}

.section-header {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
  margin-bottom: 70px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #60a5fa;
  margin-bottom: 12px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 20px;
}
.accent { color: #60a5fa; }

.subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}

.modules-grid {
  position: relative;
  z-index: 1;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  display: grid;
  gap: 32px;
  width: 100%;
  max-width: 1100px;
}

.module-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  backdrop-filter: blur(16px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.module-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(96, 165, 250, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.icon-circle {
  width: 48px;
  height: 48px;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  color: #60a5fa;
  font-size: 1.25rem;
}

.module-title {
  font-size: 1.35rem;
  font-weight: 600;
  margin-bottom: 14px;
  color: #fff;
}

.module-desc {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.7;
}

.cta-section {
  margin-top: 80px;
  position: relative;
  z-index: 1;
}

.btn-primary {
  display: inline-block;
  padding: 16px 40px;
  background: #3b82f6;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  background: #2563eb;
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

@media (max-width: 768px) {
  .tutorial-page { padding: 40px 20px 120px; }
  .title { font-size: 2.2rem; }
  .modules-grid { grid-template-columns: 1fr; }
}
</style>
