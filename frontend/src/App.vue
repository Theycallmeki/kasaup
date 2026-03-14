<script setup lang="ts">
import Sidebar from "./components/Sidebar.vue"
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