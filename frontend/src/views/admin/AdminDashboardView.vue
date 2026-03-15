<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

function goUsers() {
  router.push("/admin/users")
}

function goProviders() {
  router.push("/admin/providers")
}

function goCategories() {
  router.push("/admin/categories")
}
</script>

<template>

<div class="dashboard">

  <h1>Admin Dashboard</h1>
  <p>Manage platform users, providers, and categories.</p>

  <div class="cards">

    <div class="card">
      <h3>Users</h3>
      <p>View and manage registered users</p>
      <button @click="goUsers">Manage Users</button>
    </div>

    <div class="card">
      <h3>Providers</h3>
      <p>Verify and manage service providers</p>
      <button @click="goProviders">Manage Providers</button>
    </div>

    <div class="card">
      <h3>Categories</h3>
      <p>Manage service categories</p>
      <button @click="goCategories">Manage Categories</button>
    </div>

  </div>

</div>

</template>

<style scoped>

.dashboard{
  padding:20px;
}

.cards{
  display:flex;
  gap:20px;
  margin-top:20px;
}

.card{
  background:white;
  padding:20px;
  border-radius:8px;
  box-shadow:0 5px 15px rgba(0,0,0,0.08);
  width:220px;
}

button{
  margin-top:10px;
  padding:8px 12px;
  border:none;
  background:#ef4444;
  color:white;
  border-radius:6px;
  cursor:pointer;
}

</style>