<script setup lang="ts">
import { onMounted, computed } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "./stores/authStore"
import { useMessageStore } from "./stores/messageStore"

import Sidebar from "./components/Sidebar.vue"
import GlobalLoader from "./components/GlobalLoader.vue"
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'

const auth = useAuthStore()
const messageStore = useMessageStore()
const route = useRoute()

const hideSidebarRoutes = ["/provider/create-profile", "/auth/login", "/auth/register"]
const showSidebar = computed(() => {
  return auth.user && !hideSidebarRoutes.includes(route.path)
})

onMounted(async () => {
  const staleKeys = ["access_token", "refresh_token", "kasaup:user_location_v1", "pos_cart", "token"]
  staleKeys.forEach(key => localStorage.removeItem(key))

  await auth.fetchUser()

  if (auth.user) {
    await messageStore.fetchConversations()
    messageStore.connectWS(auth.user.id)
  }
})
</script>

<template>
  <Toast />
  <ConfirmDialog />
  <GlobalLoader />

  <div class="layout">
    <Sidebar v-if="showSidebar" />

    <main class="content">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<style>
@import "./styles/shared/notifications.css";

.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  width: 100%;
}

.content {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  padding-bottom: 120px;
  background: #0e0c1a;
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px){
  .content{
    padding-bottom: 140px;
  }
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>