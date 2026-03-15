<script setup lang="ts">
import { onMounted, ref } from "vue"
import api from "../../services/api"

const providers = ref<any[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get("/providers")
    providers.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<template>

<div>

  <h2>Providers</h2>

  <div v-if="loading">
    Loading...
  </div>

  <div v-else>

    <div
      v-for="provider in providers"
      :key="provider.id"
    >
      {{ provider.shop_name }}
    </div>

  </div>

</div>

</template>