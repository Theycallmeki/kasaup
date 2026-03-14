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

const login = async () => {

  error.value = ""
  loading.value = true

  try {

    await auth.login(email.value, password.value)

    router.push("/providers")

  } catch (err) {

    error.value = "Invalid email or password"

  } finally {

    loading.value = false

  }

}
</script>

<template>

<div class="login-container">

  <div class="login-card">

    <h1>Kasaup</h1>
    <p>Login to your account</p>

    <form @submit.prevent="login">

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        required
      />

      <button :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>

    </form>

    <p v-if="error" class="error">
      {{ error }}
    </p>

    <div class="register">

      <p>Don't have an account?</p>

      <router-link to="/auth">
        Register as Customer or Provider
      </router-link>

    </div>

  </div>

</div>

</template>

<style scoped>

.login-container{
  height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#f1f5f9;
}

.login-card{
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
  background:#2563eb;
  color:white;
  font-weight:600;
  cursor:pointer;
}

button:hover{
  background:#1d4ed8;
}

button:disabled{
  opacity:0.6;
}

.error{
  color:#ef4444;
  margin-top:10px;
}

.register{
  margin-top:20px;
}

.register a{
  color:#2563eb;
  text-decoration:none;
}

</style>
