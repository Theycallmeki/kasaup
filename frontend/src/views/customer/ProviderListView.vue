<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"

const providerStore = useProviderStore()
const router = useRouter()

onMounted(() => {
  providerStore.fetchProviders()
})

function openProvider(id: number) {
  router.push(`/providers/${id}`)
}
</script>

<template>
  <div>

    <h2>Providers</h2>

    <div v-if="providerStore.loading">
      Loading providers...
    </div>

    <div v-else>

      <div
        v-for="provider in providerStore.providers"
        :key="provider.id"
        @click="openProvider(provider.id)"
        style="cursor:pointer"
      >
        {{ provider.shop_name }}
      </div>

    </div>

  </div>
</template>