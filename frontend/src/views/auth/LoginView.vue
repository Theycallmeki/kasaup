<script setup lang="ts">
import { ref } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useScroll } from "../../hooks/useScroll"
import { useAuthStore } from "../../stores/authStore"
import { onMounted } from "vue"

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const { scrollRef: pageScroll } = useScroll()

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
    if (auth.user?.role === "provider") {
      if (auth.user?.has_profile) {
        router.push("/provider/dashboard")
      } else {
        router.push("/provider/create-profile")
      }
    }
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

onMounted(() => {
  if (route.query.error === "pending_approval") {
    error.value = "Your provider account is pending admin approval."
    isPending.value = true
  } else if (route.query.error === "google_auth_failed") {
    error.value = "Google authentication failed. Please try again."
  } else if (route.query.error === "github_auth_failed") {
    error.value = "GitHub authentication failed. Please try again."
  }
})

const googleLogin = () => {
  window.location.href = `${import.meta.env.VITE_API_URL}/auth/google`
}

const githubLogin = () => {
  window.location.href = `${import.meta.env.VITE_API_URL}/auth/github`
}
</script>

<template>
  <div class="login-page" ref="pageScroll">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="login-card">
      <span class="eyebrow">Welcome back</span>
      <h1 class="title">Kasa<span class="accent">Up</span></h1>
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

        <div class="divider">or</div>

        <button type="button" class="btn google-btn" @click="googleLogin">
          <svg width="18" height="18" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-1 .67-2.28 1.07-3.71 1.07-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.11c-.22-.66-.35-1.36-.35-2.11s.13-1.45.35-2.11V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l3.66-2.83z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
          </svg>
          Continue with Google
        </button>

        <button type="button" class="btn github-btn" @click="githubLogin">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
          </svg>
          Continue with GitHub
        </button>
      </form>

      <p class="register">
        Don't have an account?
        <router-link to="/auth">Register </router-link>
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

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 12px 0 16px;
  color: rgba(255, 255, 255, 0.2);
  font-size: 13px;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.1);
}
.divider:not(:empty)::before {
  margin-right: 12px;
}
.divider:not(:empty)::after {
  margin-left: 12px;
}

.google-btn {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 0.5px solid rgba(255, 255, 255, 0.15) !important;
  color: #fff !important;
  gap: 12px !important;
  margin-bottom: 0 !important;
}
.google-btn:hover {
  background: rgba(255, 255, 255, 0.08) !important;
}

.github-btn {
  background: #24292e !important;
  border: 0.5px solid rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
  gap: 12px !important;
  margin-top: 10px !important;
}
.github-btn:hover {
  background: #2f363d !important;
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