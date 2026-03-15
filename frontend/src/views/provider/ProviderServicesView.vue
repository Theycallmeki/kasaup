<script setup lang="ts">
import { onMounted } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useAuthStore } from "../../stores/authStore"

const serviceStore = useServiceStore()
const authStore = useAuthStore()

onMounted(() => {
  if (authStore.user?.provider_id) {
    serviceStore.fetchProviderServices(authStore.user.provider_id)
  }
})
</script>

<template>

<div>

  <h2>My Services</h2>

  <div v-if="serviceStore.loading">
    Loading...
  </div>

  <div v-else>

    <div
      v-for="service in serviceStore.services"
      :key="service.id"
    >
      {{ service.name }} - {{ service.price }}
    </div>

  </div>

</div>

</template>