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

    <Sidebar />

    <main class="content">
      <router-view />
    </main>

  </div>

</template>

<style scoped>

.layout{
  display:flex;
}

.content{
  margin-left:220px;
  padding:30px;
  width:100%;
}

</style>
