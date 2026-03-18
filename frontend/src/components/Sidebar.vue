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
<aside class="sidebar" :class="{ collapsed }" aria-label="Sidebar navigation">

  <div class="top">

    <h2 v-if="!collapsed" class="logo">Kasaup</h2>

    <button
      class="toggle"
      type="button"
      @click="toggleSidebar"
      :aria-expanded="!collapsed"
      aria-controls="sidebar-nav"
      aria-label="Toggle sidebar"
    >
      ☰
    </button>

  </div>

  <nav id="sidebar-nav" class="nav">

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

</aside>

</template>

<style scoped>

.sidebar{
  width:220px;
  height:100vh;
  background:#1e293b;
  color:white;
  padding:20px 16px;
  border-right:1px solid rgba(255,255,255,0.08);
  transition:width 0.2s ease;
  flex-shrink:0;
  display:flex;
  flex-direction:column;
  overflow:hidden;
}

.sidebar.collapsed{
  width:70px;
}

.top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:18px;
}

.logo{
  margin:0;
  font-size:18px;
  letter-spacing:0.2px;
}

.toggle{
  background:none;
  border:none;
  color:white;
  font-size:18px;
  cursor:pointer;
  padding:6px 10px;
  border-radius:8px;
}

.toggle:hover{
  background:#334155;
}

.nav{
  display:flex;
  flex-direction:column;
  gap:4px;
  overflow:auto;
  padding-right:6px;
}

.link{
  color:white;
  text-decoration:none;
  padding:8px;
  border-radius:6px;
  background:none;
  border:none;
  text-align:left;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:10px;
}

.link:hover{
  background:#334155;
}

.logout{
  color:#f87171;
}

@media (max-width: 768px){
  .sidebar{
    width:100%;
    height:auto;
    border-right:none;
    border-bottom:1px solid rgba(255,255,255,0.08);
  }

  .sidebar.collapsed{
    width:100%;
  }

  .nav{
    overflow:visible;
    padding-right:0;
  }
}

</style>
