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
      <router-view />
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
  overflow:hidden;
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
</style>