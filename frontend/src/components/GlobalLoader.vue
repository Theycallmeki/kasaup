<script setup lang="ts">
import { useLoading } from '../hooks/useLoading'

const { loadingState } = useLoading()
</script>

<template>
  <Transition name="fade">
    <div v-if="loadingState.isActive" class="loader-overlay">
      <div class="loader-container">
        <div class="glow-ring"></div>
        <div class="orbit-container">
          <div class="center-core"></div>
          <div class="orbit-ball"></div>
          <div class="orbit-ball alt"></div>
        </div>
        <p v-if="loadingState.message" class="loading-msg">{{ loadingState.message }}</p>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.loader-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(14, 12, 26, 0.75);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  position: relative;
}

.glow-ring {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.2) 0%, transparent 70%);
  filter: blur(20px);
  animation: pulse 2s ease-in-out infinite;
}

.orbit-container {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.center-core {
  width: 24px;
  height: 24px;
  background: #a78bfa;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(167, 139, 250, 0.8), 0 0 40px rgba(167, 139, 250, 0.4);
}

.orbit-ball {
  position: absolute;
  width: 10px;
  height: 10px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 0 10px #fff;
  offset-path: path('M 40,0 A 40,40 0 1 1 40,80 A 40,40 0 1 1 40,0');
  animation: orbit 1.5s linear infinite;
}

.orbit-ball.alt {
  animation-delay: -0.75s;
  background: #38bdf8;
  box-shadow: 0 0 10px #38bdf8;
}

.loading-msg {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a78bfa;
  margin: 0;
  text-shadow: 0 0 10px rgba(167, 139, 250, 0.5);
  animation: text-pulse 1.5s ease-in-out infinite;
}

@keyframes orbit {
  from { offset-distance: 0%; }
  to { offset-distance: 100%; }
}

@keyframes pulse {
  0%, 100% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
}

@keyframes text-pulse {
  0%, 100% { opacity: 0.6; transform: scale(0.98); }
  50% { opacity: 1; transform: scale(1); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
