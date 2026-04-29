<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useProviderStore } from "../../stores/providerStore"
import { useCategoryStore } from "../../stores/categoryStore"
import { useAuthStore } from "../../stores/authStore"
import { useRouter } from "vue-router"
import api from "../../services/api"
import { useLoading } from "../../hooks/useLoading"
import { useServiceFilters } from "./hooks/useServiceFilters"
import ServicesFilterPanel from "./components/ServicesFilterPanel.vue"

const router = useRouter()
const { startLoading, stopLoading } = useLoading()
const svcStore = useServiceStore()
const provStore = useProviderStore()
const catStore = useCategoryStore()
const authStore = useAuthStore()

const selected = ref<any | null>(null)
const viewingImage = ref<string | null>(null)
const currentImageIndex = ref(0)

onMounted(async () => {
  startLoading("Discovering services...")
  try {
    await Promise.all([
      svcStore.fetchServices(),
      provStore.fetchProviders(),
      catStore.fetchCategories?.() ?? Promise.resolve(),
    ])
  } finally {
    stopLoading()
  }
})

const providerMap = computed(() => {
  const m: Record<number, any> = {}
  for (const p of provStore.providers) m[p.id] = p
  return m
})

const {
  showFilters,
  query,
  tempActiveCat,
  tempSort,
  tempMinPrice,
  tempMaxPrice,
  tempMinRating,
  tempMaxDistance,
  tempUseLocation,
  locLoading,
  searching,
  filtered,
  onQuery,
  openFilters,
  cancelFilters,
  applyFilters,
  clearFilters,
  toggleLocation,
  resetAppliedFilters,
} = useServiceFilters({
  svcStore,
  providerMap,
  startLoading,
  stopLoading,
})

// Lock body scroll when modal or filters are open
watch([selected, showFilters], ([s, f]) => {
  if (s || f) {
    document.body.style.overflow = "hidden"
  } else {
    document.body.style.overflow = ""
  }
})

function goBook(svc: any) {
  const p = providerMap.value[svc.provider_id]
  if (p) router.push(`/providers/${p.id}`)
}

function selectService(svc: any) {
  selected.value = svc
  currentImageIndex.value = 0
}

function nextImage() {
  if (!selected.value?.images) return
  currentImageIndex.value = (currentImageIndex.value + 1) % selected.value.images.length
}

function prevImage() {
  if (!selected.value?.images) return
  currentImageIndex.value = (currentImageIndex.value - 1 + selected.value.images.length) % selected.value.images.length
}

const palette = ["#38bdf8", "#a78bfa", "#fbbf24", "#86efac", "#f9a8d4", "#6ee7b7", "#fb923c", "#818cf8"]
const accent = (id: number) => palette[(id ?? 0) % palette.length]
const catName = (id: number) => catStore.categories?.find((c: any) => c.id === id)?.name ?? "Service"
const shopName = (id: number) => providerMap.value[id]?.shop_name ?? "—"

const imgUrl = (path: string) => {
  if (!path) return ""
  if (path.startsWith("http")) return path
  return `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}`
}

const firstImage = (svc: any): string | null => {
  if (Array.isArray(svc.images) && svc.images.length) return imgUrl(svc.images[0].image_url)
  return null
}
</script>

<template>
  <div class="pg">

    <header class="hd">
      <div>
        <h1 class="ht">Discover Services</h1>
      </div>
      <div class="hd-r">
        <div class="ps"><b>{{ svcStore.services.length }}</b><span>Total</span></div>
        <div class="ps alt"><b>{{ provStore.providers.length }}</b><span>Providers</span></div>
      </div>
    </header>

    <div class="marketplace-layout">
      <main class="content-area">

        <div class="top-bar">
          <div class="srch-row">
            <div class="srch">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8" />
                <path d="M21 21l-4.35-4.35" />
              </svg>
              <input placeholder="Search services, providers…" :value="query"
                @input="onQuery(($event.target as HTMLInputElement).value)" />
              <span v-if="searching" class="spin" />
            </div>

            <div class="filter-wrapper">
              <button class="filter-btn" :class="{active: showFilters}" @click="showFilters ? cancelFilters() : openFilters()">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
                <span>Filters</span>
              </button>
            </div>
          </div>

          <ServicesFilterPanel
            v-show="showFilters"
            :categories="catStore.categories"
            :temp-active-cat="tempActiveCat"
            :temp-sort="tempSort"
            :temp-min-price="tempMinPrice"
            :temp-max-price="tempMaxPrice"
            :temp-min-rating="tempMinRating"
            :temp-max-distance="tempMaxDistance"
            :temp-use-location="tempUseLocation"
            :loc-loading="locLoading"
            @update:temp-active-cat="tempActiveCat = $event"
            @update:temp-sort="tempSort = $event"
            @update:temp-min-price="tempMinPrice = $event"
            @update:temp-max-price="tempMaxPrice = $event"
            @update:temp-min-rating="tempMinRating = $event"
            @update:temp-max-distance="tempMaxDistance = $event"
            @toggle-location="toggleLocation"
            @clear="clearFilters"
            @cancel="cancelFilters"
            @apply="applyFilters"
          />
        </div>

        <div v-if="svcStore.loading" class="state">
          <span class="spin-lg" />
          <p>Finding top choices…</p>
        </div>

        <div v-else-if="!filtered.length" class="state">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"
            style="color:rgba(255,255,255,0.2)">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <p>No services found matching your criteria.</p>
          <button class="rst" @click="resetAppliedFilters">Clear all filters</button>
        </div>

        <div v-else class="grid">
          <div v-for="svc in filtered" :key="svc.id" class="card" :style="{ '--a': accent(svc.category_id) }"
            @click="selectService(svc)">
            <div class="thumb" :class="{ 'no-img': !firstImage(svc) }">
              <img v-if="firstImage(svc)" :src="firstImage(svc)!" :alt="svc.name" />
              <div v-else class="img-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21 15 16 10 5 21" />
                </svg>
              </div>
              <div v-if="svc.images && svc.images.length > 1" class="multi-img-badge" title="Multiple images">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="14" height="14" rx="2" ry="2"></rect>
                  <path d="M21 7v12a2 2 0 0 1-2 2H7"></path>
                </svg>
                <span>{{ svc.images.length }}</span>
              </div>
            </div>

            <div class="c-body">
              <h3 class="ti" :title="svc.name">{{ svc.name }}</h3>
              <p class="by">{{ shopName(svc.provider_id) }}</p>

              <div class="tags">
                <span class="dur">⏱ {{ svc.duration_minutes }}m</span>
                <span class="cat-pill">{{ catName(svc.category_id) }}</span>
              </div>

              <div class="cf">
                <span class="pr">{{ Number(svc.price).toLocaleString() }}</span>
                <button class="bk" @click.stop="goBook(svc)">Book</button>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>

    <Teleport to="body">
  <div class="ov" :class="{ show: !!selected }" @click.self="selected = null">
    
    <div class="modal" v-if="selected" :style="{ '--a': accent(selected.category_id) }">
      
      <button class="mc" @click="selected = null">✕</button>

      <div class="modal-scroll">

        <div v-if="selected.images?.length" class="modal-carousel">
          <button v-if="selected.images.length > 1" @click.stop="prevImage" class="carousel-btn prev">‹</button>
          <div class="modal-carousel-track">
            <img 
              :src="imgUrl(selected.images[currentImageIndex].image_url)" 
              :alt="selected.name"
              class="modal-carousel-img" 
              @click="viewingImage = imgUrl(selected.images[currentImageIndex].image_url)" 
            />
          </div>
          <button v-if="selected.images.length > 1" @click.stop="nextImage" class="carousel-btn next">›</button>

          <div v-if="selected.images.length > 1" class="carousel-dots">
            <span 
              v-for="(_, i) in selected.images" 
              :key="i" 
              class="carousel-dot" 
              :class="{active: Number(i) === currentImageIndex}" 
              @click.stop="currentImageIndex = Number(i)"
            ></span>
          </div>
        </div>

        <span class="badge lg">{{ catName(selected.category_id) }}</span>
        <h2 class="mt">{{ selected.name }}</h2>
        <p class="mb">{{ shopName(selected.provider_id) }}</p>

        <p v-if="selected.description" class="mdesc">
          {{ selected.description }}
        </p>

        <div class="mst">
          <div><b>₱{{ Number(selected.price).toLocaleString() }}</b><em>Price</em></div>
          <div><b>{{ selected.duration_minutes }} min</b><em>Duration</em></div>
          <div><b>{{ catName(selected.category_id) }}</b><em>Category</em></div>
        </div>

        <button class="mbk" @click="goBook(selected)">
          Book This Service
        </button>

      </div>
     

    </div>

  </div>
</Teleport>

    <Teleport to="body">
      <div v-if="viewingImage" class="img-viewer-ov" @click="viewingImage = null">
        <button class="close-viewer">✕</button>
        <img :src="viewingImage" />
      </div>
    </Teleport>

   
    <div class="bottom-spacer"></div>

  </div>
</template>

<style scoped src="../../styles/customer/ServicesView.css"></style>