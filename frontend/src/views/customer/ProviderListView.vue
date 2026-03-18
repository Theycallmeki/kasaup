<script setup lang="ts">
import { onMounted, ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import ProviderMap from "../../components/ProviderMap.vue"

import InputText from "primevue/inputtext"
import Button from "primevue/button"
import Card from "primevue/card"

const providerStore = useProviderStore()
const router = useRouter()

const search = ref("")

onMounted(async () => {
  await providerStore.fetchProviders()
})

function openProvider(id: number) {
  router.push(`/providers/${id}`)
}

const filteredProviders = computed(() => {
  if (!search.value) return providerStore.providers

  return providerStore.providers.filter((p: any) =>
    p.name?.toLowerCase().includes(search.value.toLowerCase())
  )
})
</script>

<template>
  <div class="providers-page">
    <Card class="search-panel">
      <template #content>
        <div class="search-container">
          <span class="p-input-icon-left w-full">
            <i class="pi pi-search" />
            <InputText
              v-model="search"
              placeholder="Search services or providers..."
              class="w-full"
            />
          </span>

          <div class="filters">
            <Button label="All" size="small" outlined />
            <Button label="Nearby" size="small" outlined />
            <Button label="Top Rated" size="small" outlined />
          </div>
        </div>
      </template>
    </Card>

    <ProviderMap
      :providers="filteredProviders"
      @provider-click="openProvider"
    />
  </div>
</template>

<style scoped>
.providers-page {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.search-panel {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: 460px;
  border-radius: 16px;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.85);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

@media (max-width: 600px) {
  .search-panel {
    width: 90%;
  }
}
</style>