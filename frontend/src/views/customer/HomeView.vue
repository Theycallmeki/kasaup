<template>
  <div class="home">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="hero-card">
      <span class="eyebrow">Local Services</span>
      <h1 class="title">Kasa<span class="accent">up</span></h1>
      <p class="subtitle">
        Find trusted local services near you — fast, easy, and reliable.
      </p>

      <div class="actions">
        <button class="btn btn-primary" @click="goProviders">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          Browse Providers
        </button>
        <button class="btn btn-outline" @click="goAuth">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
          </svg>
          Get Started
        </button>
      </div>

      <div class="trust-dots">
        <span class="dot-item"><span class="dot" />Free to browse</span>
        <span class="dot-item"><span class="dot" />Verified providers</span>
        <span class="dot-item"><span class="dot" />Near you</span>
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

:global(html),
:global(body),
:global(#app) {
  margin: 0;
  padding: 0;
  height: 100%;
  background: #0e0c1a;
}

.home {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0e0c1a;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}
.orb1 {
  width: 420px;
  height: 420px;
  top: -80px;
  left: -100px;
  background: radial-gradient(circle, rgba(99, 60, 220, 0.35) 0%, transparent 70%);
}
.orb2 {
  width: 360px;
  height: 360px;
  bottom: -60px;
  right: -80px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.25) 0%, transparent 70%);
}

.hero-card {
  position: relative;
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 52px 44px;
  max-width: 480px;
  width: 100%;
  margin: 24px;
  text-align: center;
  backdrop-filter: blur(12px);
  animation: rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(168, 130, 255, 0.9);
  background: rgba(99, 60, 220, 0.2);
  border: 0.5px solid rgba(130, 90, 255, 0.3);
  border-radius: 100px;
  padding: 5px 14px;
  margin-bottom: 22px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin-bottom: 14px;
}
.accent {
  color: #a78bfa;
}

.subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.65;
  margin-bottom: 36px;
  max-width: 340px;
  margin-left: auto;
  margin-right: auto;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 13px 28px;
  cursor: pointer;
  border: none;
  transition: transform 0.18s ease, opacity 0.18s ease;
}
.btn:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}
.btn-primary {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
}
.btn-outline {
  background: transparent;
  border: 0.5px solid rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.75);
}

.trust-dots {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 36px;
}
.dot-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
}
.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(168, 130, 255, 0.6);
  flex-shrink: 0;
}

@keyframes rise {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (min-width: 460px) {
  .actions {
    flex-direction: row;
    justify-content: center;
  }
}
</style>