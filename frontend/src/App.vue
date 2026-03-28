<script setup lang="ts">
import { onMounted } from "vue"
import { useAuthStore } from "./stores/authStore"

import Sidebar from "./components/Sidebar.vue"

const auth = useAuthStore()

onMounted(() => {
  auth.fetchUser()
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
  .layout{
    flex-direction:column;
  }

  .content{
    height:100%;
    padding:0;
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