<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useProviderStore } from "../../stores/providerStore"
import { useCategoryStore } from "../../stores/categoryStore"
import { useAuthStore } from "../../stores/authStore"
import { searchServices } from "../../services/services"
import { useRouter } from "vue-router"
import api from "../../services/api"
import { useLoading } from "../../hooks/useLoading"

const showFilters = ref(false)
const router = useRouter()
const { startLoading, stopLoading } = useLoading()
const svcStore = useServiceStore()
const provStore = useProviderStore()
const catStore = useCategoryStore()
const authStore = useAuthStore()

const query = ref("")
const activeCat = ref<number | "all">("all")
const sort = ref("price_asc")
const minPrice = ref<number | null>(null)
const maxPrice = ref<number | null>(null)
const minRating = ref<number>(0)
const maxDistance = ref<number | null>(null)

const tempActiveCat = ref<number | "all">("all")
const tempSort = ref("price_asc")
const tempMinPrice = ref<number | null>(null)
const tempMaxPrice = ref<number | null>(null)
const tempMinRating = ref<number>(0)
const tempMaxDistance = ref<number | null>(null)
const tempUseLocation = ref(false)

const useLocation = ref(false)
const currentLat = ref<number | null>(null)
const currentLng = ref<number | null>(null)
const locLoading = ref(false)

async function fetchCurrentLocation() {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your browser")
    return
  }
  startLoading("Detecting your location...")
  locLoading.value = true
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      currentLat.value = pos.coords.latitude
      currentLng.value = pos.coords.longitude
      tempUseLocation.value = true
      locLoading.value = false
      stopLoading()
    },
    (err) => {
      console.error("Location error:", err)
      alert("Could not get your location. Please check your browser permissions.")
      tempUseLocation.value = false
      locLoading.value = false
      stopLoading()
    },
    { timeout: 10000 }
  )
}

function toggleLocation() {
  if (!tempUseLocation.value) {
    fetchCurrentLocation()
  } else {
    tempUseLocation.value = false
  }
}

function openFilters() {
  tempActiveCat.value = activeCat.value
  tempSort.value = sort.value
  tempMinPrice.value = minPrice.value
  tempMaxPrice.value = maxPrice.value
  tempMinRating.value = minRating.value
  tempMaxDistance.value = maxDistance.value
  tempUseLocation.value = useLocation.value
  showFilters.value = true
}

function cancelFilters() {
  showFilters.value = false
}

function applyFilters() {
  activeCat.value = tempActiveCat.value
  sort.value = tempSort.value
  minPrice.value = tempMinPrice.value
  maxPrice.value = tempMaxPrice.value
  minRating.value = tempMinRating.value
  maxDistance.value = tempMaxDistance.value
  useLocation.value = tempUseLocation.value
  showFilters.value = false
}

function clearFilters() {
  tempActiveCat.value = "all"
  tempSort.value = "price_asc"
  tempMinPrice.value = null
  tempMaxPrice.value = null
  tempMinRating.value = 0
  tempMaxDistance.value = null
  tempUseLocation.value = false
  tempCustomDistance.value = null
}
const tempCustomDistance = ref<number | null>(null)
const selected = ref<any | null>(null)
const searching = ref(false)
const viewingImage = ref<string | null>(null)
const currentImageIndex = ref(0)

// Lock body scroll when modal or filters are open
watch([selected, showFilters], ([s, f]) => {
  if (s || f) {
    document.body.style.overflow = "hidden"
  } else {
    document.body.style.overflow = ""
  }
})

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

const haversine = (lat1: number, lon1: number, lat2: number, lon2: number) => {
  const R = 6371 
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const filtered = computed(() => {
  let list = svcStore.services

  if (activeCat.value !== "all") {
    list = list.filter(s => s.category_id === activeCat.value)
  }

  if (query.value.trim()) {
    const q = query.value.toLowerCase()
    list = list.filter(s =>
      s.name?.toLowerCase().includes(q) ||
      s.description?.toLowerCase().includes(q) ||
      providerMap.value[s.provider_id]?.shop_name?.toLowerCase().includes(q)
    )
  }

  if (minPrice.value !== null) {
    list = list.filter(s => s.price >= (minPrice.value || 0))
  }
  if (maxPrice.value !== null) {
    list = list.filter(s => s.price <= (maxPrice.value || Infinity))
  }

  if (minRating.value > 0) {
    list = list.filter(s => {
      const p = providerMap.value[s.provider_id]
      return (p?.rating || 0) >= minRating.value
    })
  }

  if (useLocation.value && maxDistance.value !== null && currentLat.value && currentLng.value) {
    list = list.filter(s => {
      const p = providerMap.value[s.provider_id]
      if (!p?.latitude || !p?.longitude) return false
      const dist = haversine(
        currentLat.value!,
        currentLng.value!,
        p.latitude,
        p.longitude
      )
      return dist <= (maxDistance.value || Infinity)
    })
  }

  return [...list].sort((a, b) => {
    if (sort.value === "price_asc") return a.price - b.price
    if (sort.value === "price_desc") return b.price - a.price
    return a.duration_minutes - b.duration_minutes
  })
})

let debounce: ReturnType<typeof setTimeout>
function onQuery(v: string) {
  query.value = v
  clearTimeout(debounce)
  if (!v.trim()) { svcStore.fetchServices(); return }
  debounce = setTimeout(async () => {
    searching.value = true
    try {
      const p: any = { q: v }
      if (activeCat.value !== "all") p.category_id = activeCat.value
      svcStore.services = await searchServices(p)
    } finally { searching.value = false }
  }, 400)
}

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
        <p class="ey">Marketplace</p>
        <h1 class="ht">Discover Services</h1>
      </div>
      <div class="hd-r">
        <div class="ps"><b>{{ svcStore.services.length }}</b><span>Total</span></div>
        <div class="ps alt"><b>{{ provStore.providers.length }}</b><span>Providers</span></div>
      </div>
    </header>

    <div class="marketplace-layout">
      <!-- Main Content Grid -->
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

          <!-- Horizontal filter panel below the search bar -->
          <div v-show="showFilters" class="filter-panel">
            <div class="fp-sections">
              <div class="filter-group">
                <h4>Category</h4>
                <div class="filter-pills">
                  <button class="fp" :class="{active: tempActiveCat === 'all'}" @click="tempActiveCat = 'all'">All Categories</button>
                  <button class="fp" v-for="cat in catStore.categories" :key="cat.id" 
                          :class="{active: tempActiveCat === cat.id}" @click="tempActiveCat = cat.id">
                    {{ cat.name }}
                  </button>
                </div>
              </div>
              
              <div class="filter-group">
                <h4>Sort By</h4>
                <div class="filter-pills">
                  <button class="fp" :class="{active: tempSort === 'price_asc'}" @click="tempSort = 'price_asc'">Price: Low to High</button>
                  <button class="fp" :class="{active: tempSort === 'price_desc'}" @click="tempSort = 'price_desc'">Price: High to Low</button>
                  <button class="fp" :class="{active: tempSort === 'duration'}" @click="tempSort = 'duration'">Duration</button>
                </div>
              </div>

              <div class="filter-group">
                <h4>Price Range</h4>
                <div class="filter-inputs">
                  <div class="input-with-symbol">
                    <span>₱</span>
                    <input type="number" v-model.number="tempMinPrice" placeholder="Min" />
                  </div>
                  <div class="input-divider">—</div>
                  <div class="input-with-symbol">
                    <span>₱</span>
                    <input type="number" v-model.number="tempMaxPrice" placeholder="Max" />
                  </div>
                </div>
              </div>

              <div class="filter-group">
                <h4>Minimum Rating</h4>
                <div class="filter-pills">
                  <button class="fp" :class="{active: tempMinRating === 0}" @click="tempMinRating = 0">Any Rating</button>
                  <button class="fp" v-for="r in [5, 4, 3, 2]" :key="r" :class="{active: tempMinRating === r}" @click="tempMinRating = r">
                    {{ r }}★ & Up
                  </button>
                </div>
              </div>

              <div class="filter-group">
                <div class="fg-head">
                  <h4>Distance Range</h4>
                  <button class="toggle-switch" :class="{on: tempUseLocation, loading: locLoading}" @click="toggleLocation" type="button" :disabled="locLoading">
                    <span class="switch-ball"></span>
                  </button>
                </div>
                
                <div v-if="tempUseLocation" class="filter-pills">
                  <button class="fp" :class="{active: tempMaxDistance === null}" @click="tempMaxDistance = null">Anywhere</button>
                  <button class="fp" :class="{active: tempMaxDistance === 5}" @click="tempMaxDistance = 5">5km</button>
                  <button class="fp" :class="{active: tempMaxDistance === 10}" @click="tempMaxDistance = 10">10km</button>
                  <button class="fp" :class="{active: tempMaxDistance === 25}" @click="tempMaxDistance = 25">25km</button>
                  <div class="custom-dist-input">
                    <input 
                      type="number" 
                      v-model="tempMaxDistance" 
                      placeholder="Custom"
                      class="cd-input"
                    />
                    <span class="unit">km</span>
                  </div>
                </div>
                <div v-else class="loc-off-msg">
                   {{ locLoading ? 'Getting your location...' : 'Turn on to find services near you.' }}
                </div>
              </div>
            </div>

            <div class="fp-actions">
              <button class="f-btn f-clear" @click="clearFilters">Clear All</button>
              <button class="f-btn f-cancel" @click="cancelFilters">Cancel</button>
              <button class="f-btn f-apply" @click="applyFilters">Apply Filters</button>
            </div>
          </div>
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
          <button class="rst" @click="query = ''; activeCat = 'all'; minPrice = null; maxPrice = null; minRating = 0; maxDistance = null; svcStore.fetchServices()">Clear all filters</button>
        </div>

        <div v-else class="grid">
          <div v-for="svc in filtered" :key="svc.id" class="card" :style="{ '--a': accent(svc.category_id) }"
            @click="selectService(svc)">
            <!-- Image top half -->
            <div class="thumb" :class="{ 'no-img': !firstImage(svc) }">
              <img v-if="firstImage(svc)" :src="firstImage(svc)!" :alt="svc.name" />
              <div v-else class="img-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21 15 16 10 5 21" />
                </svg>
              </div>
            </div>

            <!-- Details below -->
            <div class="c-body">
              <h3 class="ti" :title="svc.name">{{ svc.name }}</h3>
              <p class="by">{{ shopName(svc.provider_id) }}</p>

              <div class="tags">
                <span class="dur">⏱ {{ svc.duration_minutes }}m</span>
                <span class="cat-pill">{{ catName(svc.category_id) }}</span>
              </div>

              <!-- Price & Book row -->
              <div class="cf">
                <span class="pr">{{ Number(svc.price).toLocaleString() }}</span>
                <button class="bk" @click.stop="goBook(svc)">Book</button>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>

    <!-- Modal for Preview -->
    <Teleport to="body">
  <div class="ov" :class="{ show: !!selected }" @click.self="selected = null">
    
    <div class="modal" v-if="selected" :style="{ '--a': accent(selected.category_id) }">
      
      <!-- CLOSE BUTTON stays outside scroll -->
      <button class="mc" @click="selected = null">✕</button>

      <!-- 🔥 SCROLL WRAPPER START -->
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
      <!-- 🔥 SCROLL WRAPPER END -->

    </div>

  </div>
</Teleport>

    <!-- Fullscreen Image Viewer -->
    <Teleport to="body">
      <div v-if="viewingImage" class="img-viewer-ov" @click="viewingImage = null">
        <button class="close-viewer">✕</button>
        <img :src="viewingImage" />
      </div>
    </Teleport>

    <!-- Direct spacer to the bottom of the list -->
    <div class="bottom-spacer"></div>

  </div>
</template>

<style scoped src="../../styles/customer/ServicesView.css"></style>