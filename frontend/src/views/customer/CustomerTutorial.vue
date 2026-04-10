<script setup lang="ts">
import { ref } from 'vue'
import { useScroll } from "../../hooks/useScroll"

const { scrollRef: pageScroll } = useScroll()

const steps = [
  {
    title: "Browse Services",
    desc: "Explore a wide range of local services including cleaning, repairs, and beauty.",
    icon: "search"
  },
  {
    title: "Pick a Provider",
    desc: "View provider profiles, read reviews, and check their location on the map.",
    icon: "map"
  },
  {
    title: "Book Instantly",
    desc: "Choose a date and time that works for you. No more endless phone calls.",
    icon: "calendar"
  },
  {
    title: "Chat & Coordinate",
    desc: "Communicate directly with your service provider via our built-in chat.",
    icon: "message"
  }
]
</script>

<template>
  <div class="page tutorial-page" ref="pageScroll">
    <!-- Background Orbs -->
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <header class="section-header">
      <div class="eyebrow">Getting Started</div>
      <h1 class="title">How to use Kasa<span class="accent">Up</span></h1>
      <p class="subtitle">Follow these simple steps to find and book the best local service providers.</p>
    </header>

    <div class="steps-grid">
      <div v-for="(step, index) in steps" :key="index" class="step-card">
        <div class="step-num">{{ index + 1 }}</div>
        <div class="step-content">
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.desc }}</p>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <router-link to="/services" class="btn-primary">Start Browsing Now</router-link>
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

.bg-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
  opacity: 0.4;
  z-index: 0;
}
.orb1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -200px;
  background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
}
.orb2 {
  width: 300px;
  height: 300px;
  bottom: -50px;
  right: -100px;
  background: radial-gradient(circle, #a855f7 0%, transparent 70%);
}

.section-header {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 600px;
  margin-bottom: 60px;
}

.eyebrow {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: #a78bfa;
  margin-bottom: 12px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 20px;
}
.accent { color: #a78bfa; }

.subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}

.steps-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1200px;
}

.step-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  gap: 24px;
  backdrop-filter: blur(12px);
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.step-card:hover {
  transform: translateY(-8px);
  border-color: rgba(167, 139, 250, 0.3);
}

.step-num {
  font-family: 'Sora', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: rgba(167, 139, 250, 0.2);
  line-height: 1;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #fff;
}

.step-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
}

.cta-section {
  margin-top: 80px;
  position: relative;
  z-index: 1;
}

.btn-primary {
  display: inline-block;
  padding: 16px 40px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  font-weight: 600;
  text-decoration: none;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.3);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(124, 58, 237, 0.4);
}

@media (max-width: 768px) {
  .tutorial-page { padding: 40px 20px 120px; }
  .title { font-size: 2rem; }
  .steps-grid { grid-template-columns: 1fr; }
}
</style>
