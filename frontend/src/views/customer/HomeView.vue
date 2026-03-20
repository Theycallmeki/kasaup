<template>
  <div class="home">
    <div class="hero-card">
      <h1 class="title">Kasaup</h1>
      <p class="subtitle">
        Find trusted local services near you — fast, easy, and reliable
      </p>

      <div class="actions">
        <Button 
          label="Browse Providers" 
          icon="pi pi-search"
          class="p-button-lg p-button-primary"
          @click="goProviders"
        />

        <Button 
          label="Get Started" 
          icon="pi pi-user"
          class="p-button-lg p-button-outlined"
          @click="goAuth"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import Button from "primevue/button"

const router = useRouter()

const goProviders = () => {
  router.push("/providers")
}

const goAuth = () => {
  router.push("/auth")
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #4f46e5, #9333ea);
  padding: 20px;
}

.hero-card {
  background: white;
  padding: 50px 40px;
  border-radius: 20px;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.6s ease;
}

.title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #111827;
}

.subtitle {
  font-size: 1.1rem;
  color: #6b7280;
  margin-bottom: 30px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.p-button {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.p-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 640px) {
  .actions {
    flex-direction: row;
    justify-content: center;
  }
}
</style>