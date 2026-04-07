<script setup lang="ts">
import { ref, computed, onMounted } from "vue"

const props = defineProps<{
  categories: any[]
  activeCat: number | "all"
}>()

const emit = defineEmits<{
  "update:activeCat": [v: number | "all"]
}>()

const isExpanded = ref(false)

onMounted(() => {
  if (window.innerWidth > 800) {
    isExpanded.value = true
  }
})

const activeCatName = computed(() => {
  if (props.activeCat === 'all') return 'All Services'
  const c = props.categories.find(c => c.id === props.activeCat)
  return c ? c.name : 'All Services'
})

const handleSelect = (val: number | "all") => {
  emit('update:activeCat', val)
  if (window.innerWidth <= 800) {
    isExpanded.value = false
  }
}
</script>

<template>
  <div class="sidebar-filters">
    <div class="filter-section">
      <h3 class="fs-title" @click="isExpanded = !isExpanded" style="cursor: pointer; justify-content: space-between; user-select: none;">
        <div style="display:flex; align-items:center; gap:8px;">
          <svg viewBox="0 0 24 24" fill="none" class="icon-h" stroke="currentColor" stroke-width="2">
            <line x1="8" y1="6" x2="21" y2="6"/>
            <line x1="8" y1="12" x2="21" y2="12"/>
            <line x1="8" y1="18" x2="21" y2="18"/>
            <line x1="3" y1="6" x2="3.01" y2="6"/>
            <line x1="3" y1="12" x2="3.01" y2="12"/>
            <line x1="3" y1="18" x2="3.01" y2="18"/>
          </svg>
          Categories
        </div>
        <svg :style="{ transform: isExpanded ? 'rotate(180deg)' : 'rotate(0)' }"
             style="transition: 0.2s; width: 16px; height: 16px; color: rgba(255,255,255,0.4);"
             viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </h3>
      
      <ul class="cat-list" v-if="categories.length">
        <template v-if="isExpanded">
          <li>
            <button 
              class="cat-item" 
              :class="{ active: activeCat === 'all' }" 
              @click="handleSelect('all')"
            >
              <span class="bullet" />
              All Services
            </button>
          </li>
          <li v-for="cat in categories" :key="cat.id">
            <button 
              class="cat-item" 
              :class="{ active: activeCat === cat.id }" 
              @click="handleSelect(cat.id)"
            >
              <span class="bullet" />
              {{ cat.name }}
            </button>
          </li>
        </template>
        
        <template v-else>
          <li>
            <button class="cat-item active" @click="isExpanded = true">
              <span class="bullet" />
              {{ activeCatName }}
            </button>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.sidebar-filters {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px 16px;
  transition: all 0.3s ease;
}

@media (max-width: 800px) {
  .sidebar-filters {
    background: transparent;
    border: none;
    padding: 0;
    gap: 12px;
  }

  .fs-title {
    background: rgba(255, 255, 255, 0.04);
    border: 0.5px solid rgba(255, 255, 255, 0.08) !important;
    padding: 12px 16px !important;
    border-radius: 10px;
    margin-bottom: 0 !important;
  }

  .fs-title:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  .cat-list {
    background: rgba(18, 16, 30, 0.95);
    border: 1px solid rgba(167, 139, 250, 0.2);
    border-radius: 12px;
    padding: 12px;
    margin-top: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    position: relative;
    z-index: 10;
  }
}

.filter-section {
  display: flex;
  flex-direction: column;
}
.fs-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Sora', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px 0;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 14px;
  transition: background 0.2s;
}
.icon-h {
  width: 18px;
  height: 18px;
  color: #a78bfa;
}
.cat-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.cat-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.55);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}
.cat-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
}
.cat-item.active {
  background: rgba(167, 139, 250, 0.15);
  color: #c4b5fd;
}
.bullet {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  transition: all 0.2s;
}
.cat-item:hover .bullet {
  border-color: rgba(255, 255, 255, 0.8);
}
.cat-item.active .bullet {
  background: #a78bfa;
  border-color: #a78bfa;
  box-shadow: 0 0 8px rgba(167, 139, 250, 0.6);
}
</style>