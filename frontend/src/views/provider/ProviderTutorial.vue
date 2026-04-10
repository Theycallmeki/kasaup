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

<style scoped>
.tutorial-page {
  position: relative;
  min-height: 100%;
  padding: 80px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  overflow-x: hidden;
  background: #0e0c1a;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  scrollbar-width: thin;
  scrollbar-color: rgba(167, 139, 250, 0.2) transparent;
}

.tutorial-page::-webkit-scrollbar {
  width: 6px;
}
.tutorial-page::-webkit-scrollbar-track {
  background: transparent;
}
.tutorial-page::-webkit-scrollbar-thumb {
  background: rgba(167, 139, 250, 0.2);
  border-radius: 10px;
}
.tutorial-page::-webkit-scrollbar-thumb:hover {
  background: rgba(167, 139, 250, 0.4);
}

.section-header {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
  margin-bottom: 70px;
}

.eyebrow {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #a78bfa;
  margin-bottom: 12px;
  opacity: 0.9;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 3.2rem;
  font-weight: 700;
  margin: 0 0 20px;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.accent { color: #a78bfa; }

.subtitle {
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
}

.modules-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
  width: 100%;
  max-width: 1100px;
}

.module-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 24px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.module-card:hover {
  transform: translateY(-10px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(167, 139, 250, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.icon-circle {
  width: 48px;
  height: 48px;
  background: rgba(167, 139, 250, 0.1);
  border: 1px solid rgba(167, 139, 250, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  color: #a78bfa;
  font-size: 1.25rem;
}

.module-title {
  font-size: 1.35rem;
  font-weight: 600;
  margin-bottom: 14px;
  color: #fff;
  letter-spacing: -0.01em;
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
  padding: 18px 48px;
  background: #7c3aed;
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(124, 58, 237, 0.25);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-primary:hover {
  transform: translateY(-2px);
  background: #6d28d9;
  box-shadow: 0 15px 40px rgba(124, 58, 237, 0.35);
  border-color: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .tutorial-page { padding: 60px 24px 140px; }
  .title { 
    font-size: 2.2rem; 
    line-height: 1.2;
    margin-bottom: 16px;
  }
  .subtitle { font-size: 1rem; }
  .section-header { margin-bottom: 40px; }
  .modules-grid { grid-template-columns: 1fr; gap: 20px; }
  .module-card { padding: 32px 24px; gap: 20px; }
  .cta-section { margin-top: 60px; }
  .btn-primary { width: 100%; text-align: center; padding: 16px; }
}
</style>
