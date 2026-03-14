<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuthStore } from "../stores/authStore"

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref("")
const password = ref("")
const full_name = ref("")
const phone = ref("")
const loading = ref(false)
const error = ref("")

const role = computed(() => route.query.role || "customer")

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

<div class="register-container">

  <div class="register-card">

    <h1>Kasaup</h1>
    <p>Create your {{ role }} account</p>

    <form @submit.prevent="register">

      <input
        v-model="full_name"
        placeholder="Full Name"
        required
      />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        required
      />

      <input
        v-model="phone"
        placeholder="Phone"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button :disabled="loading">
        {{ loading ? "Creating account..." : "Register" }}
      </button>

    </form>

    <p v-if="error" class="error">
      {{ error }}
    </p>

    <div class="login">

      <p>Already have an account?</p>

      <router-link to="/login">
        Login
      </router-link>

    </div>

  </div>

</div>

</template>

<style scoped>

.register-container{
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:#f1f5f9;
}

.register-card{
  width:380px;
  padding:40px;
  background:white;
  border-radius:10px;
  box-shadow:0 10px 30px rgba(0,0,0,0.1);
  text-align:center;
}

form{
  display:flex;
  flex-direction:column;
  margin-top:20px;
}

input{
  padding:10px;
  margin-bottom:12px;
  border-radius:6px;
  border:1px solid #cbd5e1;
}

button{
  padding:10px;
  border:none;
  border-radius:6px;
  background:#16a34a;
  color:white;
  font-weight:600;
  cursor:pointer;
}

button:hover{
  background:#15803d;
}

.error{
  color:#ef4444;
  margin-top:10px;
}

.login{
  margin-top:20px;
}

.login a{
  color:#2563eb;
  text-decoration:none;
}

</style>
