<template>
  <component :is="isMobile ? MobileHomeView : DesktopHomeView" />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, shallowRef } from 'vue'
import DesktopHomeView from './DesktopHomeView.vue'
import MobileHomeView from './MobileHomeView.vue'

const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>