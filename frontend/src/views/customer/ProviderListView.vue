<script setup lang="ts">
import { onMounted } from "vue"
import { useRouter } from "vue-router"
import { useProviderStore } from "../../stores/providerStore"
import ProviderMap from "../../components/ProviderMap.vue"

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

<div class="providers-page">

  <div class="search-bar">
    <input placeholder="Search services or providers..." />
  </div>

  <ProviderMap />

</div>

</template>

<style scoped>

.providers-page{
  position:relative;
  height:100vh;
  width:100%;
}

.search-bar{
  position:absolute;
  top:20px;
  left:50%;
  transform:translateX(-50%);
  z-index:1000;
  width:420px;
}

.search-bar input{
  width:100%;
  padding:12px 16px;
  border-radius:10px;
  border:1px solid #cbd5e1;
  box-shadow:0 5px 15px rgba(0,0,0,0.15);
  font-size:14px;
}

</style>