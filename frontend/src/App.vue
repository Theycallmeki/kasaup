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

  <main
    class="content"
  >
    <router-view />
  </main>

</div>

</template>

<style scoped>

.layout{
  display:flex;
}

.content{
  padding:30px;
  width:100%;
  min-height:100vh;
  background:#f8fafc;
  flex:1;
}

@media (max-width: 768px){
  .layout{
    flex-direction:column;
  }

  .content{
    min-height:0;
    padding:16px;
  }
}

</style>