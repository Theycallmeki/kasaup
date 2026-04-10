<script setup lang="ts">
import { useRouter } from "vue-router"
import { useScroll } from "../../hooks/useScroll"

const router = useRouter()
const { scrollRef: pageScroll } = useScroll()

const goCustomer = () => router.push("/register?role=customer")
const goProvider = () => router.push("/register?role=provider")
</script>

<template>
  <div class="auth-page" ref="pageScroll">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="auth-card">
      <span class="eyebrow">Welcome</span>
      <h1 class="title">Kasa<span class="accent">Up</span></h1>
      <p class="subtitle">Find trusted local services near you</p>

      <button class="btn btn-outline" @click="goCustomer">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
        </svg>
        Create Customer Account
      </button>
 
      <button class="btn btn-outline" @click="goProvider">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
        </svg>
        Become a Service Provider
      </button>

      <p class="footer">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

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

.auth-page {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0e0c1a;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

@media (max-width: 480px) {
  .auth-page {
    position: relative;
    min-height: 100svh;
    overflow-y: auto;
    align-items: flex-start;
    padding: 40px 0 48px;
  }
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

.auth-card {
  position: relative;
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 48px 40px;
  max-width: 420px;
  width: calc(100% - 48px);
  text-align: center;
  backdrop-filter: blur(12px);
  animation: rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 36px 24px 32px;
    border-radius: 20px;
    width: calc(100% - 32px);
    margin: auto;
  }
}

@media (max-width: 360px) {
  .auth-card {
    padding: 28px 18px 28px;
  }
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
  margin-bottom: 20px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}
.accent {
  color: #a78bfa;
}

.subtitle {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 32px;
}

@media (max-width: 480px) {
  .title { font-size: 2rem; }
  .subtitle { margin-bottom: 24px; }
  .orb1 { width: 260px; height: 260px; }
  .orb2 { width: 220px; height: 220px; }
  .btn { font-size: 0.9rem; padding: 12px 16px; }
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 13px 20px;
  cursor: pointer;
  border: none;
  transition: transform 0.18s ease, opacity 0.18s ease;
  margin-bottom: 10px;
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
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
}

.btn-google {
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  gap: 12px;
  margin-bottom: 24px;
}
.btn-google:hover {
  background: rgba(255, 255, 255, 0.08);
}

.btn-google-alt {
  background: rgba(255, 255, 255, 0.03);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  gap: 10px;
  font-size: 0.9rem;
  margin-top: -4px;
}
.btn-google-alt:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.footer {
  margin-top: 24px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
}
.footer a {
  color: rgba(167, 139, 250, 0.8);
  text-decoration: none;
  margin-left: 4px;
}
.footer a:hover {
  color: #a78bfa;
}

@keyframes rise {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>