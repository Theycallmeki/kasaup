<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useProviderStore } from "../../stores/providerStore"
import { useCategoryStore } from "../../stores/categoryStore"
import { searchServices } from "../../services/services"
import { useRouter } from "vue-router"
import ServiceFilters from "../../components/ServiceFilters.vue"
import api from "../../services/api"

const router    = useRouter()
const svcStore  = useServiceStore()
const provStore = useProviderStore()
const catStore  = useCategoryStore()

const query     = ref("")
const activeCat = ref<number | "all">("all")
const sort      = ref("price_asc")
const selected  = ref<any | null>(null)
const searching = ref(false)

onMounted(async () => {
  await Promise.all([
    svcStore.fetchServices(),
    provStore.fetchProviders(),
    catStore.fetchCategories?.() ?? Promise.resolve(),
  ])
})

const providerMap = computed(() => {
  const m: Record<number, any> = {}
  for (const p of provStore.providers) m[p.id] = p
  return m
})

const filtered = computed(() => {
  let list = svcStore.services
  if (activeCat.value !== "all") list = list.filter(s => s.category_id === activeCat.value)
  if (query.value.trim()) {
    const q = query.value.toLowerCase()
    list = list.filter(s =>
      s.name?.toLowerCase().includes(q) ||
      s.description?.toLowerCase().includes(q) ||
      providerMap.value[s.provider_id]?.shop_name?.toLowerCase().includes(q)
    )
  }
  return [...list].sort((a, b) => {
    if (sort.value === "price_asc")  return a.price - b.price
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

const palette  = ["#38bdf8","#a78bfa","#fbbf24","#86efac","#f9a8d4","#6ee7b7","#fb923c","#818cf8"]
const accent   = (id: number) => palette[(id ?? 0) % palette.length]
const catName  = (id: number) => catStore.categories?.find((c: any) => c.id === id)?.name ?? "Service"
const shopName = (id: number) => providerMap.value[id]?.shop_name ?? "—"

const imgUrl = (path: string) =>
  path ? `${api.defaults.baseURL}${path.startsWith("/") ? path : "/" + path}` : ""

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
          <div class="srch">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
            </svg>
            <input
              placeholder="Search services, providers…"
              :value="query"
              @input="onQuery(($event.target as HTMLInputElement).value)"
            />
            <span v-if="searching" class="spin" />
          </div>

          <div class="sort-tabs">
            <span class="sort-label">Sort by:</span>
            <button class="st" :class="{active: sort === 'price_asc'}" @click="sort = 'price_asc'">Price: Low to High</button>
            <button class="st" :class="{active: sort === 'price_desc'}" @click="sort = 'price_desc'">Price: High to Low</button>
            <button class="st" :class="{active: sort === 'duration'}" @click="sort = 'duration'">Duration</button>
          </div>
        </div>

        <div v-if="svcStore.loading" class="state">
          <span class="spin-lg" /><p>Finding top choices…</p>
        </div>

        <div v-else-if="!filtered.length" class="state">
          <span>🔍</span>
          <p>No services found matching your criteria.</p>
          <button class="rst" @click="query=''; activeCat='all'; svcStore.fetchServices()">Clear all filters</button>
        </div>

        <div v-else class="grid">
          <div
            v-for="svc in filtered" :key="svc.id"
            class="card" :style="{ '--a': accent(svc.category_id) }"
            @click="selected = svc"
          >
            <!-- Image top half -->
            <div class="thumb" :class="{'no-img': !firstImage(svc)}">
              <img v-if="firstImage(svc)" :src="firstImage(svc)!" :alt="svc.name" />
              <div v-else class="img-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
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

      <!-- Right Sidebar for Filters -->
      <aside class="sidebar">
        <ServiceFilters 
          :categories="catStore.categories ?? []"
          :activeCat="activeCat"
          @update:activeCat="activeCat = $event"
        />
      </aside>

    </div>

    <!-- Modal for Preview -->
    <Teleport to="body">
      <div class="ov" :class="{ show: !!selected }" @click.self="selected = null">
        <div class="modal" v-if="selected" :style="{ '--a': accent(selected.category_id) }">
          <button class="mc" @click="selected = null">✕</button>

          <div v-if="selected.images?.length" class="modal-gallery">
            <img
              v-for="(img, i) in selected.images"
              :key="i"
              :src="imgUrl(img.image_url)"
              :alt="selected.name"
              class="modal-thumb"
            />
          </div>

          <span class="badge lg">{{ catName(selected.category_id) }}</span>
          <h2 class="mt">{{ selected.name }}</h2>
          <p class="mb">{{ shopName(selected.provider_id) }}</p>
          <p v-if="selected.description" class="mdesc">{{ selected.description }}</p>

          <div class="mst">
            <div><b>₱{{ Number(selected.price).toLocaleString() }}</b><em>Price</em></div>
            <div><b>{{ selected.duration_minutes }} min</b><em>Duration</em></div>
            <div><b>{{ catName(selected.category_id) }}</b><em>Category</em></div>
          </div>

          <button class="mbk" @click="goBook(selected)">Book This Service</button>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<style scoped src="../../styles/customer/ServicesView.css"></style>