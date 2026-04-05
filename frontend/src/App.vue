<script setup lang="ts">
import { onMounted } from "vue"
import { useAuthStore } from "./stores/authStore"
import { useMessageStore } from "./stores/messageStore"

import Sidebar from "./components/Sidebar.vue"

const auth = useAuthStore()
const messageStore = useMessageStore()

onMounted(async () => {
  // Check for tokens in URL (Auth Handshake for Universal Login)
  const urlParams = new URLSearchParams(window.location.search)
  const accessToken = urlParams.get("access_token")
  const refreshToken = urlParams.get("refresh_token")

  if (accessToken && refreshToken) {
    // Save tokens as cookies on the frontend domain
    // We set Secure and SameSite=Lax for production compatibility
    const secure = window.location.protocol === "https:" ? "Secure;" : ""
    document.cookie = `access_token=${accessToken}; path=/; max-age=900; ${secure} SameSite=Lax`
    document.cookie = `refresh_token=${refreshToken}; path=/; max-age=604800; ${secure} SameSite=Lax`

    // Clean the URL
    const cleanUrl = window.location.pathname + window.location.hash
    window.history.replaceState({}, document.title, cleanUrl)
  }

  await auth.fetchUser()
  // Once the user is authenticated, connect WS and fetch conversations globally
  // so the sidebar unread badge works in real-time from any page
  if (auth.user) {
    await messageStore.fetchConversations()
    messageStore.connectWS(auth.user.id)
  }
})
</script>

<template>
  <div class="layout">
    <Sidebar v-if="auth.user" />

    <main class="content">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<style scoped>
.layout{
  display:flex;
  height:100vh;
  width:100vw;
  overflow:hidden;
}

.content{
  flex:1;
  height:100%;
  margin:0;
  padding:0;
  background:#0e0c1a;
  overflow-y:auto;
}

.content::-webkit-scrollbar {
  width: 8px;
}
.content::-webkit-scrollbar-track {
  background: transparent;
}
.content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px){
  /* sidebar is hidden via Sidebar.vue, layout stays row */
  .layout{
    flex-direction: row;
  }

  .content{
    height: 100%;
    padding: 0;
    /* prevent content from hiding under the fixed bottom nav */
    padding-bottom: 64px;
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