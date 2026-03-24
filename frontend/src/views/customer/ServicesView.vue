<script setup lang="ts">
import { ref, computed, onMounted } from "vue"
import { useServiceStore } from "../../stores/serviceStore"
import { useProviderStore } from "../../stores/providerStore"
import { useCategoryStore } from "../../stores/categoryStore"
import { searchServices } from "../../services/services"
import { useRouter } from "vue-router"
import ServiceFilters from "../../components/ServiceFilters.vue"

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

const BASE_URL = "http://localhost:8000"

const imgUrl = (path: string) => `${BASE_URL}/${path}`

const firstImage = (svc: any): string | null => {
  if (Array.isArray(svc.images) && svc.images.length) return imgUrl(svc.images[0].image_url)
  return null
}
</script>

<template>
  <div class="pg">

    <!-- Header -->
    <header class="hd">
      <div>
        <p class="ey">Discover</p>
        <h1 class="ht">Services</h1>
      </div>
      <div class="hd-r">
        <div class="ps"><b>{{ svcStore.services.length }}</b><span>Total</span></div>
        <div class="ps alt"><b>{{ provStore.providers.length }}</b><span>Providers</span></div>
      </div>
    </header>

    <!-- Filters -->
    <ServiceFilters
      :categories="catStore.categories ?? []"
      :searching="searching"
      @update:query="onQuery"
      @update:activeCat="activeCat = $event"
      @update:sort="sort = $event"
    />

    <!-- Loading -->
    <div v-if="svcStore.loading" class="state">
      <span class="spin" /><p>Loading services…</p>
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" class="state">
      <span>🔍</span>
      <p>No services found.</p>
      <button class="rst" @click="query=''; activeCat='all'; svcStore.fetchServices()">Clear filters</button>
    </div>

    <!-- Grid -->
    <div v-else class="grid">
      <div
        v-for="svc in filtered" :key="svc.id"
        class="card" :style="{ '--a': accent(svc.category_id) }"
        @click="selected = svc"
      >
        <div v-if="firstImage(svc)" class="thumb">
          <img :src="firstImage(svc)!" :alt="svc.name" />
          <div class="thumb-fade" />
        </div>
        <div class="ct">
          <span class="badge">{{ catName(svc.category_id) }}</span>
          <span class="dur">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
            </svg>
            {{ svc.duration_minutes }} min
          </span>
        </div>
        <h3 class="ti">{{ svc.name }}</h3>
        <p class="by">{{ shopName(svc.provider_id) }}</p>
        <p v-if="svc.description" class="desc">{{ svc.description }}</p>
        <div class="cf">
          <span class="pr">₱{{ Number(svc.price).toLocaleString() }}</span>
          <button class="bk" @click.stop="goBook(svc)">Book</button>
        </div>
        <div class="glow" />
      </div>
    </div>

    <!-- Modal -->
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

.pg { min-height:100vh; background:#0e0c1a; color:#e8e8f0; padding:36px 28px 64px; font-family:'DM Sans',sans-serif; }

.hd { display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:24px; gap:16px; flex-wrap:wrap; }
.ey { font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:#a78bfa; margin:0 0 4px; font-weight:600; }
.ht { font-family:'Sora',sans-serif; font-size:clamp(1.6rem,4vw,2.4rem); font-weight:700; margin:0; letter-spacing:-.03em; color:#fff; }
.hd-r { display:flex; gap:10px; }
.ps { display:flex; flex-direction:column; align-items:center; background:rgba(255,255,255,.05); border:0.5px solid rgba(255,255,255,.08); border-radius:12px; padding:10px 20px; }
.ps b { font-family:'Sora',sans-serif; font-size:1.4rem; line-height:1; color:#fff; }
.ps span { font-size:10px; color:rgba(255,255,255,.35); margin-top:3px; }
.ps.alt { background:rgba(99,60,220,.12); border-color:rgba(130,90,255,.2); }
.ps.alt b { color:#c4b5fd; }

.state { display:flex; flex-direction:column; align-items:center; gap:12px; padding:80px 20px; color:rgba(255,255,255,.35); font-size:.9rem; }
.spin { display:inline-block; width:26px; height:26px; border:3px solid rgba(255,255,255,.1); border-top-color:#a78bfa; border-radius:50%; animation:sp .6s linear infinite; }
@keyframes sp { to { transform:rotate(360deg) } }
.rst { padding:8px 20px; border-radius:8px; background:rgba(99,60,220,.2); border:0.5px solid rgba(130,90,255,.3); color:#c4b5fd; cursor:pointer; font-family:'DM Sans',sans-serif; font-size:.875rem; }

.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(268px,1fr)); gap:14px; }

.card { position:relative; background:rgba(255,255,255,.03); border:0.5px solid rgba(255,255,255,.08); border-radius:16px; overflow:hidden; cursor:pointer; transition:transform .2s,border-color .2s; display:flex; flex-direction:column; }
.card:hover { transform:translateY(-2px); border-color:color-mix(in srgb,var(--a) 30%,transparent); }
.card > .ct, .card > .ti, .card > .by, .card > .desc, .card > .cf { padding-left:20px; padding-right:20px; }
.card > .ct { padding-top:16px; }
.card > .cf { padding-bottom:16px; }
.glow { position:absolute; bottom:-40px; right:-40px; width:110px; height:110px; border-radius:50%; background:color-mix(in srgb,var(--a) 8%,transparent); filter:blur(28px); pointer-events:none; }

.thumb { position:relative; width:100%; height:148px; flex-shrink:0; }
.thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.thumb-fade { position:absolute; inset:0; background:linear-gradient(to bottom, transparent 40%, #0e0c1a 100%); }

.ct { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.badge { font-size:10px; font-weight:600; letter-spacing:.08em; text-transform:uppercase; padding:3px 10px; border-radius:100px; color:var(--a); background:color-mix(in srgb,var(--a) 12%,transparent); }
.badge.lg { font-size:11px; padding:4px 12px; margin-bottom:10px; display:inline-block; }
.dur { display:flex; align-items:center; gap:4px; font-size:11px; color:rgba(255,255,255,.35); }
.dur svg { width:12px; height:12px; }

.ti { font-family:'Sora',sans-serif; font-size:.95rem; font-weight:700; margin:0 0 3px; color:#fff; line-height:1.3; }
.by { font-size:.8rem; color:rgba(255,255,255,.33); margin:0 0 8px; }
.desc { font-size:.82rem; color:rgba(255,255,255,.4); line-height:1.5; margin:0 0 12px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; flex:1; }

.cf { display:flex; align-items:center; justify-content:space-between; margin-top:auto; padding-top:12px; border-top:0.5px solid rgba(255,255,255,.06); }
.pr { font-family:'Sora',sans-serif; font-size:1.1rem; font-weight:700; color:#fff; }
.bk { padding:7px 16px; border-radius:8px; border:0.5px solid color-mix(in srgb,var(--a) 35%,transparent); background:color-mix(in srgb,var(--a) 12%,transparent); color:var(--a); font-family:'DM Sans',sans-serif; font-size:.82rem; font-weight:600; cursor:pointer; transition:all .15s; }
.bk:hover { background:color-mix(in srgb,var(--a) 22%,transparent); }

.ov { position:fixed; inset:0; background:rgba(0,0,0,.65); backdrop-filter:blur(8px); z-index:999; display:flex; align-items:center; justify-content:center; padding:20px; opacity:0; pointer-events:none; transition:opacity .25s; }
.ov.show { opacity:1; pointer-events:all; }
.modal { background:#1a1730; border:0.5px solid rgba(130,90,255,.25); border-radius:20px; padding:32px; max-width:440px; width:100%; position:relative; transform:translateY(12px); transition:transform .25s cubic-bezier(.34,1.56,.64,1); max-height:85vh; overflow-y:auto; }
.ov.show .modal { transform:translateY(0); }
.mc { position:absolute; top:16px; right:16px; background:rgba(255,255,255,.07); border:0.5px solid rgba(255,255,255,.1); border-radius:8px; width:30px; height:30px; color:rgba(255,255,255,.5); cursor:pointer; display:flex; align-items:center; justify-content:center; transition:color .15s; }
.mc:hover { color:#fff; }

.modal-gallery { display:flex; gap:8px; overflow-x:auto; margin-bottom:18px; padding-bottom:4px; scroll-snap-type:x mandatory; }
.modal-gallery::-webkit-scrollbar { height:3px; }
.modal-gallery::-webkit-scrollbar-track { background:rgba(255,255,255,.05); border-radius:2px; }
.modal-gallery::-webkit-scrollbar-thumb { background:rgba(130,90,255,.4); border-radius:2px; }
.modal-thumb { width:140px; height:100px; object-fit:cover; border-radius:10px; flex-shrink:0; scroll-snap-align:start; border:0.5px solid rgba(255,255,255,.08); }

.mt { font-family:'Sora',sans-serif; font-size:1.4rem; font-weight:700; margin:0 0 4px; color:#fff; letter-spacing:-.02em; }
.mb { font-size:.85rem; color:rgba(255,255,255,.35); margin:0 0 16px; }
.mdesc { font-size:.88rem; color:rgba(255,255,255,.5); line-height:1.6; margin:0 0 20px; }
.mst { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:22px; }
.mst > div { background:rgba(255,255,255,.04); border:0.5px solid rgba(255,255,255,.07); border-radius:10px; padding:12px; text-align:center; }
.mst b { display:block; font-family:'Sora',sans-serif; font-size:1rem; font-weight:700; color:#fff; margin-bottom:3px; }
.mst em { font-size:10px; color:rgba(255,255,255,.3); font-style:normal; }
.mbk { width:100%; padding:12px; border-radius:12px; border:none; background:linear-gradient(135deg,rgba(99,60,220,.8),rgba(130,90,255,.7)); color:#fff; font-family:'DM Sans',sans-serif; font-size:.9rem; font-weight:600; cursor:pointer; transition:all .15s; box-shadow:0 4px 18px rgba(99,60,220,.3); }
.mbk:hover { transform:translateY(-1px); box-shadow:0 6px 24px rgba(99,60,220,.45); }

@media(max-width:600px) {
  .pg { padding:24px 16px 48px; }
  .grid { grid-template-columns:1fr; }
  .mst { grid-template-columns:repeat(2,1fr); }
}
</style>