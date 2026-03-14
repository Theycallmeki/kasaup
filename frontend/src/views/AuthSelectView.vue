<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

const goLogin = () => {
  router.push("/login")
}

const goCustomer = () => {
  router.push("/register?role=customer")
}

const goProvider = () => {
  router.push("/register?role=provider")
}
</script>

<template>

<div class="auth-container">

  <div class="auth-card">

    <h1 class="logo">Kasaup</h1>
    <p class="subtitle">Find trusted local services</p>

    <button class="login-btn" @click="goLogin">
      Login
    </button>

    <div class="divider">
      or
    </div>

    <button class="customer-btn" @click="goCustomer">
      Create Customer Account
    </button>

    <button class="provider-btn" @click="goProvider">
      Become a Service Provider
    </button>

  </div>

</div>

</template>

<style scoped>

.auth-container{
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:#f1f5f9;
}

.auth-card{
  width:420px;
  padding:40px;
  background:white;
  border-radius:10px;
  box-shadow:0 10px 30px rgba(0,0,0,0.1);
  text-align:center;
}

.logo{
  margin-bottom:10px;
}

.subtitle{
  color:#64748b;
  margin-bottom:30px;
}

button{
  width:100%;
  padding:12px;
  border:none;
  border-radius:6px;
  margin-bottom:10px;
  font-weight:600;
  cursor:pointer;
}

.login-btn{
  background:#2563eb;
  color:white;
}

.login-btn:hover{
  background:#1d4ed8;
}

.customer-btn{
  background:#16a34a;
  color:white;
}

.customer-btn:hover{
  background:#15803d;
}

.provider-btn{
  background:#f59e0b;
  color:white;
}

.provider-btn:hover{
  background:#d97706;
}

.divider{
  margin:15px 0;
  color:#94a3b8;
}

</style>
