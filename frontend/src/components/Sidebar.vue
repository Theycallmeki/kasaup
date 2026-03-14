<script setup lang="ts">
import { ref } from "vue"
import { useAuthStore } from "../stores/authStore"
import { useRouter } from "vue-router"

const auth = useAuthStore()
const router = useRouter()

const collapsed = ref(false)

const toggleSidebar = () => {
  collapsed.value = !collapsed.value
}

const logout = async () => {
  await auth.logout()
  router.push("/login")
}
</script>

<template>

  <div :class="['sidebar', { collapsed }]">

    <div class="top">

      <h2 v-if="!collapsed" class="logo">
        Kasaup
      </h2>

      <button class="toggle" @click="toggleSidebar">
        ☰
      </button>

    </div>

    <nav>

      <router-link to="/" class="link">
        <span v-if="!collapsed">Home</span>
      </router-link>

      <router-link to="/providers" class="link">
        <span v-if="!collapsed">Providers</span>
      </router-link>

      <router-link to="/appointments" class="link">
        <span v-if="!collapsed">Appointments</span>
      </router-link>

      <button class="link logout" @click="logout">
        <span v-if="!collapsed">Logout</span>
      </button>

    </nav>

  </div>

</template>

<style scoped>

.sidebar{
  width:220px;
  height:100vh;
  background:#1e293b;
  color:white;
  padding:20px;
  position:fixed;
  transition:width 0.2s ease;
}

.sidebar.collapsed{
  width:70px;
}

.top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:30px;
}

.toggle{
  background:none;
  border:none;
  color:white;
  font-size:18px;
  cursor:pointer;
}

nav{
  display:flex;
  flex-direction:column;
}

.link{
  color:white;
  text-decoration:none;
  margin:10px 0;
  padding:8px;
  border-radius:6px;
  background:none;
  border:none;
  text-align:left;
  cursor:pointer;
}

.link:hover{
  background:#334155;
}

.logout{
  color:#f87171;
}

</style>
