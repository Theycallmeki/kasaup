<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuthStore } from "../../stores/authStore"

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref("")
const password = ref("")
const full_name = ref("")
const phone = ref("")
const loading = ref(false)
const error = ref("")
const showPassword = ref(false)

const role = computed(() => (route.query.role as string) || "customer")

const register = async () => {
  error.value = ""
  loading.value = true

  try {
    await auth.register({
      email: email.value,
      password: password.value,
      full_name: full_name.value,
      phone: phone.value,
      role: role.value
    })

    router.push("/login")
  } catch (err: any) {
    error.value = "Registration failed. Email may already exist."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="bg-orb orb1" />
    <div class="bg-orb orb2" />

    <div class="register-card">
      <span class="eyebrow">Create account</span>
      <h1 class="title">Kasa<span class="accent">up</span></h1>
      <p class="subtitle">Registering as a <span class="role-label">{{ role }}</span></p>

      <form @submit.prevent="register">
        <input
          v-model="full_name"
          class="field"
          placeholder="Full Name"
          required
        />
        <input
          v-model="email"
          class="field"
          type="email"
          placeholder="Email"
          required
        />
        <input
          v-model="phone"
          class="field"
          placeholder="Phone"
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

        <p v-if="error" class="error">{{ error }}</p>

        <button class="btn" :disabled="loading">
          <svg v-if="!loading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <line x1="19" y1="8" x2="19" y2="14" />
            <line x1="22" y1="11" x2="16" y2="11" />
          </svg>
          {{ loading ? "Creating account..." : "Register" }}
        </button>
      </form>

      <p class="footer">
        Already have an account?
        <router-link to="/login">Login</router-link>
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

.register-page {
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

.register-card {
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
  margin-bottom: 28px;
}
.role-label {
  color: rgba(167, 139, 250, 0.8);
  text-transform: capitalize;
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