<script setup lang="ts">
import { ref, computed } from "vue"
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

const role = computed(() => auth.user?.role)

const menus = {
  customer: [
    { label: "Providers", path: "/providers" },
    { label: "My Appointments", path: "/appointments" }
  ],

  provider: [
    { label: "Dashboard", path: "/provider/dashboard" },
    { label: "Services", path: "/provider/services" },
    { label: "Appointments", path: "/provider/appointments" },
    { label: "Availability", path: "/provider/availability" }
  ],

  admin: [
    { label: "Dashboard", path: "/admin/dashboard" },
    { label: "Users", path: "/admin/users" },
    { label: "Providers", path: "/admin/providers" },
    { label: "Categories", path: "/admin/categories" }
  ]
}

const menuItems = computed(() => {
  if (!role.value) return []
  return menus[role.value as keyof typeof menus] || []
})
</script>

<template>

<div :class="['sidebar', { collapsed }]" v-if="auth.user">

  <div class="top">

    <h2 v-if="!collapsed" class="logo">
      Kasaup
    </h2>

    <button class="toggle" @click="toggleSidebar">
      ☰
    </button>

  </div>

  <nav>

    <router-link
      v-for="item in menuItems"
      :key="item.path"
      :to="item.path"
      class="link"
    >
      <span v-if="!collapsed">{{ item.label }}</span>
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
