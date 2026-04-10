<script setup lang="ts">
import { ref, computed } from "vue"
import { useScroll } from "../hooks/useScroll"
import { useAuthStore } from "../stores/authStore"
import { useMessageStore } from "../stores/messageStore"
import { useRouter } from "vue-router"

const auth = useAuthStore()
const messageStore = useMessageStore()
const router = useRouter()
const { scrollRef: navScroll } = useScroll()

const collapsed = ref(false)
const mobileDrawerOpen = ref(false)

const toggleSidebar = () => {
  collapsed.value = !collapsed.value
}

const toggleMobileDrawer = () => {
  mobileDrawerOpen.value = !mobileDrawerOpen.value
}

const closeMobileDrawer = () => {
  mobileDrawerOpen.value = false
}

const logout = async () => {
  mobileDrawerOpen.value = false
  await auth.logout()
  router.push("/login")
}

const role = computed(() => auth.user?.role)

const menus = {
  customer: [
    { label: "Services",         path: "/services",             icon: "search"   },
    { label: "Providers",        path: "/providers",            icon: "map"      },
    { label: "Appointments",         path: "/appointments",         icon: "calendar" },
    { label: "History",          path: "/appointments/history", icon: "clock"    },
    { label: "Messages",         path: "/messages",             icon: "message"  },
    { label: "Profile",          path: "/profile",              icon: "user"     }
  ],
  provider: [
    { label: "Dashboard",    path: "/provider/dashboard",    icon: "grid"     },
    { label: "Services",     path: "/provider/services",     icon: "wrench"   },
    { label: "Appointments", path: "/provider/appointments", icon: "calendar" },
    { label: "Availability", path: "/provider/availability", icon: "clock"    },
    { label: "Messages",     path: "/messages",             icon: "message"  },
    { label: "Profile",      path: "/provider/profile",      icon: "users"    }
  ],
  admin: [
    { label: "Dashboard",  path: "/admin/dashboard",  icon: "grid"   },
    { label: "Users",      path: "/admin/users",       icon: "users"  },
    { label: "Providers",  path: "/admin/providers",   icon: "wrench" },
    { label: "Categories", path: "/admin/categories",  icon: "tag"    }
  ]
}

const menuItems = computed(() => {
  if (!role.value) return []
  return menus[role.value as keyof typeof menus] || []
})

const icons: Record<string, string> = {
  grid:     "M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
  search:   "M11 11m-8 0a8 8 0 1 0 16 0 8 8 0 1 0-16 0M21 21l-4.35-4.35",
  map:      "M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4zM8 2v16M16 6v16",
  calendar: "M3 4h18v18H3zM16 2v4M8 2v4M3 10h18",
  clock:    "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM12 6v6l4 2",
  wrench:   "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z",
  users:    "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
  tag:      "M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82zM7 7h.01",
  message:  "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z",
  logout:   "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9",
  menu:     "M3 12h18M3 6h18M3 18h18",
  user:     "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
  close:    "M18 6L6 18M6 6l12 12"
}
</script>

<template>
  <!-- ═══════════════════════════════════
       DESKTOP: vertical sidebar
  ═══════════════════════════════════ -->
  <aside
    class="sidebar"
    :class="{ collapsed }"
    aria-label="Sidebar navigation"
  >
    <div class="top">
      <div v-if="!collapsed" class="logo">Kasa<span class="accent">Up</span></div>
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

    <div v-if="!collapsed && role" class="role-badge">{{ role }}</div>

    <nav id="sidebar-nav" class="nav" ref="navScroll">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="link"
        active-class="active"
      >
        <div class="link-content">
          <div class="icon-wrapper">
             <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
               <path :d="icons[item.icon]" />
             </svg>
             <div v-if="item.label === 'Messages' && messageStore.totalUnreadCount > 0 && collapsed" class="unread-dot mini"></div>
          </div>
          <span v-if="!collapsed" class="link-label">{{ item.label }}</span>
          
          <div v-if="item.label === 'Messages' && messageStore.totalUnreadCount > 0 && !collapsed" class="unread-dot pill"></div>
        </div>
      </router-link>

      <button class="link logout" @click="logout">
        <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="icons.logout" />
        </svg>
        <span v-if="!collapsed" class="link-label">Logout</span>
      </button>
    </nav>
  </aside>

  <!-- ═══════════════════════════════════
       MOBILE: bottom navigation bar
  ═══════════════════════════════════ -->
  <nav class="mobile-bottom-nav" aria-label="Mobile navigation">
    <router-link
      v-for="item in menuItems"
      :key="item.path"
      :to="item.path"
      class="mob-link"
      active-class="mob-active"
    >
      <div class="mob-icon-container">
        <svg class="mob-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="icons[item.icon]" />
        </svg>
        <div v-if="item.label === 'Messages' && messageStore.totalUnreadCount > 0" class="unread-dot mob"></div>
      </div>
      <span class="mob-label">{{ item.label }}</span>
    </router-link>

    <!-- More / Logout button -->
    <button class="mob-link mob-logout" @click="toggleMobileDrawer" aria-label="More options">
      <svg class="mob-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path :d="mobileDrawerOpen ? icons.close : icons.menu" />
      </svg>
      <span class="mob-label">More</span>
    </button>
  </nav>

  <!-- Mobile drawer overlay -->
  <Transition name="drawer-fade">
    <div v-if="mobileDrawerOpen" class="mob-overlay" @click="closeMobileDrawer">
      <div class="mob-drawer" @click.stop>
        <div class="mob-drawer-header">
          <div class="logo">Kasa<span class="accent">up</span></div>
          <div v-if="role" class="role-badge">{{ role }}</div>
        </div>
        <button class="mob-drawer-logout" @click="logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path :d="icons.logout" />
          </svg>
          Logout
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.sidebar {
  width: 200px;
  height: 100vh;
  background: #0e0c1a;
  border-right: 0.5px solid rgba(255, 255, 255, 0.08);
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  transition: width 0.25s cubic-bezier(0.22, 1, 0.36, 1);
  flex-shrink: 0;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

.sidebar.collapsed {
  width: 54px;
}

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
.accent { color: #a78bfa; }

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
.link.active .link-icon { opacity: 1; }

.link-label { overflow: hidden; }

.logout { color: rgba(248, 113, 113, 0.6) !important; }
.logout:hover {
  background: rgba(248, 113, 113, 0.08) !important;
  color: #f87171 !important;
}

.link-content {
  display: flex;
  align-items: center;
  gap: inherit;
  flex: 1;
  position: relative;
}

.unread-dot {
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
  animation: pulse-green 2s infinite;
}

.unread-dot.pill {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
}

.unread-dot.mini {
  width: 5px;
  height: 5px;
  position: absolute;
  top: -2px;
  right: -2px;
}

.icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.unread-dot.mob {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 10px;
  height: 10px;
}

.mob-icon-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@media (max-width: 768px) {
  /* Hide desktop sidebar on mobile */
  .sidebar { display: none; }
}

/* ════════════════════════════════════════
   MOBILE BOTTOM NAV BAR
════════════════════════════════════════ */
.mobile-bottom-nav {
  display: none;
}

@media (max-width: 768px) {
  .mobile-bottom-nav {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background: rgba(14, 12, 26, 0.97);
    border-top: 0.5px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    height: 64px;
    padding: 0 4px;
    padding-bottom: env(safe-area-inset-bottom);
    justify-content: space-around;
    align-items: center;
  }

  .mob-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    flex: 1;
    height: 100%;
    padding: 6px 4px;
    color: rgba(255, 255, 255, 0.4);
    text-decoration: none;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.6rem;
    font-weight: 500;
    border: none;
    background: none;
    cursor: pointer;
    border-radius: 12px;
    transition: color 0.15s, background 0.15s;
    letter-spacing: 0.01em;
    white-space: nowrap;
  }

  .mob-link:hover,
  .mob-link:focus {
    color: rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.05);
    outline: none;
  }

  .mob-link.mob-active {
    color: #c4b5fd;
    background: rgba(99, 60, 220, 0.15);
  }

  .mob-icon {
    width: 22px;
    height: 22px;
    flex-shrink: 0;
    opacity: 0.7;
    transition: opacity 0.15s;
  }
  .mob-link:hover .mob-icon,
  .mob-link.mob-active .mob-icon {
    opacity: 1;
  }

  .mob-label {
    font-size: 0.58rem;
    line-height: 1;
  }

  .mob-logout .mob-icon { color: rgba(248, 113, 113, 0.7); }
  .mob-logout { color: rgba(248, 113, 113, 0.6) !important; }
  .mob-logout:hover { color: #f87171 !important; background: rgba(248,113,113,0.08) !important; }
}

/* ════════════════════════════════════════
   MOBILE DRAWER (More panel)
════════════════════════════════════════ */
.mob-overlay {
  display: none;
}

@media (max-width: 768px) {
  .mob-overlay {
    display: flex;
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    align-items: flex-end;
    justify-content: stretch;
  }

  .mob-drawer {
    width: 100%;
    background: #13112a;
    border-top: 0.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px 20px 0 0;
    padding: 24px 20px;
    padding-bottom: calc(80px + env(safe-area-inset-bottom));
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .mob-drawer-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
  }

  .mob-drawer-logout {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 16px;
    border-radius: 12px;
    color: rgba(248, 113, 113, 0.8);
    background: rgba(248, 113, 113, 0.08);
    border: 0.5px solid rgba(248, 113, 113, 0.2);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    width: 100%;
    text-align: left;
    transition: background 0.15s, color 0.15s;
  }
  .mob-drawer-logout:hover { background: rgba(248,113,113,0.15); color: #f87171; }
  .mob-drawer-logout svg { width: 18px; height: 18px; flex-shrink: 0; }
}

/* ════════════════════════════════════════
   DRAWER TRANSITION
════════════════════════════════════════ */
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
.drawer-fade-enter-active .mob-drawer,
.drawer-fade-leave-active .mob-drawer {
  transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}
.drawer-fade-enter-from .mob-drawer,
.drawer-fade-leave-to .mob-drawer {
  transform: translateY(100%);
}
</style>