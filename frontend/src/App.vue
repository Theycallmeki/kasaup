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

    <!-- Sidebar only when logged in -->
    <Sidebar v-if="auth.user" />

    <main
      class="content"
      :class="{ full: !auth.user }"
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
  margin-left:220px;
  padding:30px;
  width:100%;
}

.full{
  margin-left:0;
}

</style>
