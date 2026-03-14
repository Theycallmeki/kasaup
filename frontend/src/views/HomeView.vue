<template>
  <div class="home">

    <h1>Kasaup</h1>
    <p>Find trusted local services near you</p>

    <div class="actions">
      <button @click="goProviders">Browse Providers</button>
      <button @click="goAuth">Get Started</button>
    </div>

  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"

const router = useRouter()

const goProviders = () => {
  router.push("/providers")
}

const goAuth = () => {
  router.push("/auth")
}
</script>

<style scoped>

.home{
  text-align:center;
  margin-top:100px;
}

.actions{
  margin-top:30px;
}

button{
  margin:10px;
  padding:10px 20px;
}

</style>
