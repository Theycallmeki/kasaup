<script setup lang="ts">
import { onMounted, ref } from "vue"
import api from "../../services/api"

const users = ref<any[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get("/users")
    users.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<template>

<div>

  <h2>Users</h2>

  <div v-if="loading">
    Loading...
  </div>

  <div v-else>

    <div
      v-for="user in users"
      :key="user.id"
    >
      {{ user.email }} - {{ user.role }}
    </div>

  </div>

</div>

</template>