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
    { label: "Providers",        path: "/providers",            icon: "search" },
    { label: "My Appointments",  path: "/appointments",         icon: "calendar" },
    { label: "Booking History",  path: "/appointments/history", icon: "clock" }
  ],
  provider: [
    { label: "Dashboard",     path: "/provider/dashboard",    icon: "grid" },
    { label: "Services",      path: "/provider/services",     icon: "wrench" },
    { label: "Appointments",  path: "/provider/appointments", icon: "calendar" },
    { label: "Availability",  path: "/provider/availability", icon: "clock" }
  ],
  admin: [
    { label: "Dashboard",   path: "/admin/dashboard",   icon: "grid" },
    { label: "Users",       path: "/admin/users",       icon: "users" },
    { label: "Providers",   path: "/admin/providers",   icon: "wrench" },
    { label: "Categories",  path: "/admin/categories",  icon: "tag" }
  ]
}

const menuItems = computed(() => {
  if (!role.value) return []
  return menus[role.value as keyof typeof menus] || []
})

// SVG paths keyed by icon name
const icons: Record<string, string> = {
  grid:     "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
  search:   "M11 11m-8 0a8 8 0 1 0 16 0 8 8 0 1 0-16 0M21 21l-4.35-4.35",
  calendar: "M3 4h18v18H3zM16 2v4M8 2v4M3 10h18",
  clock:    "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM12 6v6l4 2",
  wrench:   "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z",
  users:    "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
  tag:      "M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82zM7 7h.01",
  logout:   "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"
}
</script>

<template>
  <aside
    class="sidebar"
    :class="{ collapsed }"
    aria-label="Sidebar navigation"
  >
    <!-- Top -->
    <div class="top">
      <div v-if="!collapsed" class="logo">Kasa<span class="accent">up</span></div>
      <button
        class="toggle"
        type="button"
        @click="toggleSidebar"
        :aria-expanded="!collapsed"
        aria-label="Toggle sidebar"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>
    </div>

    <!-- Role badge -->
    <div v-if="!collapsed && role" class="role-badge">{{ role }}</div>

    <!-- Nav -->
    <nav id="sidebar-nav" class="nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="link"
        active-class="active"
      >
        <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="icons[item.icon]" />
        </svg>
        <span v-if="!collapsed" class="link-label">{{ item.label }}</span>
      </router-link>

      <button class="link logout" @click="logout">
        <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="icons.logout" />
        </svg>
        <span v-if="!collapsed" class="link-label">Logout</span>
      </button>
    </nav>
  </aside>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.sidebar {
  width: 220px;
  height: 100vh;
  background: #0e0c1a;
  border-right: 0.5px solid rgba(255, 255, 255, 0.08);
  padding: 24px 14px;
  display: flex;
  flex-direction: column;
  transition: width 0.25s cubic-bezier(0.22, 1, 0.36, 1);
  flex-shrink: 0;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

.sidebar.collapsed {
  width: 66px;
}

/* Top row */
.top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  min-height: 36px;
}

.logo {
  font-family: 'Sora', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
  white-space: nowrap;
}
.accent {
  color: #a78bfa;
}

.toggle {
  background: rgba(255, 255, 255, 0.05);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.5);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
}
.toggle:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Role badge */
.role-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(168, 130, 255, 0.8);
  background: rgba(99, 60, 220, 0.15);
  border: 0.5px solid rgba(130, 90, 255, 0.25);
  border-radius: 100px;
  padding: 3px 10px;
  margin-bottom: 20px;
  align-self: flex-start;
}

/* Nav */
.nav {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  overflow: hidden;
}

.link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
  overflow: hidden;
}
.link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.9);
}
.link.active {
  background: rgba(99, 60, 220, 0.2);
  color: #c4b5fd;
  border: 0.5px solid rgba(130, 90, 255, 0.2);
}

.link-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  opacity: 0.7;
}
.link:hover .link-icon,
.link.active .link-icon {
  opacity: 1;
}

.link-label {
  overflow: hidden;
}

.logout {
  color: rgba(248, 113, 113, 0.6) !important;
}
.logout:hover {
  background: rgba(248, 113, 113, 0.08) !important;
  color: #f87171 !important;
}

/* Mobile */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    border-right: none;
    border-bottom: 0.5px solid rgba(255, 255, 255, 0.08);
  }
  .sidebar.collapsed {
    width: 100%;
  }
  .nav {
    overflow: visible;
  }
}
</style>