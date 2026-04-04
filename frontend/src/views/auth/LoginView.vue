<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../../stores/authStore"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)
const showPassword = ref(false)
const isPending = ref(false)

const login = async () => {
  error.value = ""
  loading.value = true

  try {
    await auth.login(email.value, password.value)

    if (auth.user?.role === "customer") router.push("/providers")
    if (auth.user?.role === "provider") router.push("/provider/dashboard")
    if (auth.user?.role === "admin") router.push("/admin/dashboard")
  } catch (err: any) {
    if (err.response?.status === 403) {
      error.value = err.response.data.detail || "Your provider account is pending admin approval."
      isPending.value = true
    } else {
      error.value = "Invalid email or password"
      isPending.value = false
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="login-card">
      <span class="eyebrow">Welcome back</span>
      <h1 class="title">Kasa<span class="accent">up</span></h1>
      <p class="subtitle">Login to your account</p>

      <form @submit.prevent="login">
        <input
          v-model="email"
          class="field"
          type="email"
          placeholder="Email"
          required
          autofocus
        />
        <div class="password-wrapper">
          <input
            v-model="password"
            class="field pr-field"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            required
          />
          <button type="button" class="toggle-password" @click="showPassword = !showPassword">
            <svg v-if="showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <line x1="2" y1="2" x2="22" y2="22" />
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </button>
        </div>

        <p v-if="error && isPending" class="pending-warning">{{ error }}</p>
        <p v-else-if="error" class="error">{{ error }}</p>

        <button class="btn" :disabled="loading">
          <svg v-if="!loading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
            <polyline points="10 17 15 12 10 7" />
            <line x1="15" y1="12" x2="3" y2="12" />
          </svg>
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <p class="register">
        Don't have an account?
        <router-link to="/auth">Register as Customer or Provider</router-link>
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

.login-page {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0e0c1a;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

/* ── Responsive overrides ── */
@media (max-width: 480px) {
  .login-page {
    position: relative;
    min-height: 100svh;
    overflow-y: auto;
    align-items: flex-start;
    padding: 32px 0 40px;
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

.login-card {
  position: relative;
  background: rgba(255, 255, 255, 0.035);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 48px 40px;
  max-width: 400px;
  width: calc(100% - 48px);
  text-align: center;
  backdrop-filter: blur(12px);
  animation: rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@media (max-width: 480px) {
  .login-card {
    padding: 36px 24px 32px;
    border-radius: 20px;
    width: calc(100% - 32px);
    margin: auto;
  }
}

@media (max-width: 360px) {
  .login-card {
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

@media (max-width: 480px) {
  .title { font-size: 2rem; }
  .subtitle { margin-bottom: 20px; }
  .orb1 { width: 260px; height: 260px; }
  .orb2 { width: 220px; height: 220px; }
}

.subtitle {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 28px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.field {
  width: 100%;
  box-sizing: border-box;
  padding: 13px 16px;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.18s;
}
.field::placeholder {
  color: rgba(255, 255, 255, 0.25);
}
.field:focus {
  border-color: rgba(167, 139, 250, 0.5);
}

.password-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}
.pr-field {
  padding-right: 40px !important;
}
.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.18s;
}
.toggle-password:hover {
  color: #fff;
}

.error {
  font-size: 13px;
  color: #f87171;
  text-align: left;
  margin-top: -4px;
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
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: #fff;
  transition: transform 0.18s ease, opacity 0.18s ease;
  margin-top: 4px;
}
.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  opacity: 0.9;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.register {
  margin-top: 24px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
}
.register a {
  color: rgba(167, 139, 250, 0.8);
  text-decoration: none;
  margin-left: 4px;
}
.register a:hover {
  color: #a78bfa;
}

@keyframes rise {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.pending-warning {
  font-size: 13px;
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.08);
  border: 0.5px solid rgba(245, 158, 11, 0.25);
  border-radius: 10px;
  padding: 12px 14px;
  text-align: left;
  line-height: 1.5;
}
</style>