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
  margin-bottom: 60px;
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

.steps-grid {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1200px;
}

.step-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  gap: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.step-card:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(167, 139, 250, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.step-num {
  font-family: 'Sora', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: rgba(167, 139, 250, 0.25);
  line-height: 1;
}

.step-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #fff;
  letter-spacing: -0.01em;
}

.step-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.6;
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
  .steps-grid { grid-template-columns: 1fr; gap: 16px; }
  .step-card { padding: 24px; gap: 16px; }
  .step-num { font-size: 1.8rem; }
  .cta-section { margin-top: 60px; }
  .btn-primary { width: 100%; text-align: center; padding: 16px; }
}
</style>
