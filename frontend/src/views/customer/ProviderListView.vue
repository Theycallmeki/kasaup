<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { useProviderStore } from "../../stores/providerStore"
import ProviderMap from "../../components/ProviderMap.vue"
import {
  normalizeText,
  scoreProviderQuery,
  SEARCH_MATCH_THRESHOLD,
} from "../../utils/providerSearch"
import { getCategories } from "../../services/categories"

const providerStore = useProviderStore()

const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)

const searchDraft = ref("")
const activeSearchQuery = ref("")
const pinnedProviderId = ref<number | null>(null)

const suggestionsOpen = ref(false)
const highlightIndex = ref(0)
const inputFocused = ref(false)

const USER_LOCATION_KEY = "kasaup:user_location_v1"

const SUGGESTION_LIMIT = 8

const categories = ref<{ id: number; name: string }[]>([])
/** Empty string = all categories; otherwise category id as string for the select’s v-model. */
const categoryFilter = ref("")

function providerHasCategory(p: Record<string, unknown>, categoryName: string): boolean {
  const names = Array.isArray(p.category_names) ? (p.category_names as string[]) : []
  const t = normalizeText(categoryName)
  return names.some((n) => normalizeText(n) === t)
}

function persistUserLocation(lat: number, lng: number) {
  try {
    localStorage.setItem(USER_LOCATION_KEY, JSON.stringify({ lat, lng }))
  } catch (e) {
    console.warn("Unable to persist user location:", e)
  }
}

function restoreUserLocation() {
  try {
    const raw = localStorage.getItem(USER_LOCATION_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw) as { lat?: unknown; lng?: unknown }
    if (typeof parsed.lat === "number" && typeof parsed.lng === "number") {
      userLat.value = parsed.lat
      userLng.value = parsed.lng
    }
  } catch (e) {
    console.warn("Unable to restore user location:", e)
  }
}

function haversine(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLon = ((lon2 - lon1) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

function useMyLocation() {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your browser.")
    return
  }

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat.value = pos.coords.latitude
      userLng.value = pos.coords.longitude
      persistUserLocation(userLat.value, userLng.value)
    },
    (err) => {
      console.error("Geolocation error:", err)
      alert(err.message || "Unable to get your location.")
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  )
}

function locationLine(p: Record<string, unknown>): string {
  const addr = typeof p.address === "string" && p.address.trim() ? p.address.trim() : null
  const dist =
    typeof p.distance_km === "number" ? `${p.distance_km.toFixed(1)} km away` : null
  if (addr && dist) return `${addr} · ${dist}`
  if (addr) return addr
  if (dist) return dist
  if (typeof p.latitude === "number" && typeof p.longitude === "number") {
    return `${p.latitude.toFixed(4)}, ${p.longitude.toFixed(4)}`
  }
  return "Location not set"
}

function categoryLabel(p: Record<string, unknown>): string | null {
  const cats = Array.isArray(p.category_names) ? (p.category_names as string[]) : []
  if (!cats.length) return null
  return cats.join(" · ")
}

function runSearch() {
  pinnedProviderId.value = null
  activeSearchQuery.value = searchDraft.value.trim()
  suggestionsOpen.value = false
}

function clearSearch() {
  searchDraft.value = ""
  activeSearchQuery.value = ""
  categoryFilter.value = ""
  pinnedProviderId.value = null
  suggestionsOpen.value = false
}

function selectSuggestion(p: Record<string, unknown>) {
  const id = Number(p.id)
  if (!Number.isFinite(id)) return
  pinnedProviderId.value = id
  searchDraft.value = typeof p.shop_name === "string" ? p.shop_name : ""
  activeSearchQuery.value = ""
  suggestionsOpen.value = false
}

function onSearchFocus() {
  inputFocused.value = true
  if (searchDraft.value.trim().length > 0) suggestionsOpen.value = true
}

function onSearchBlur() {
  inputFocused.value = false
  window.setTimeout(() => {
    suggestionsOpen.value = false
  }, 180)
}

function onSearchInput() {
  pinnedProviderId.value = null
  highlightIndex.value = 0
  if (searchDraft.value.trim().length > 0) suggestionsOpen.value = true
  else suggestionsOpen.value = false
}

function onSearchKeydown(e: KeyboardEvent) {
  const list = suggestions.value
  const open = showSuggestionDropdown.value

  if (e.key === "Escape") {
    suggestionsOpen.value = false
    return
  }

  if (!open || !list.length) return

  if (e.key === "ArrowDown") {
    e.preventDefault()
    highlightIndex.value = Math.min(highlightIndex.value + 1, list.length - 1)
    return
  }
  if (e.key === "ArrowUp") {
    e.preventDefault()
    highlightIndex.value = Math.max(highlightIndex.value - 1, 0)
    return
  }
  if (e.key === "Enter") {
    e.preventDefault()
    const p = list[highlightIndex.value]
    if (p) selectSuggestion(p)
    else runSearch()
  }
}

onMounted(async () => {
  restoreUserLocation()
  await Promise.all([
    providerStore.fetchProviders(),
    getCategories({ limit: 500, offset: 0 })
      .then((data: { id: number; name: string }[]) => {
        categories.value = Array.isArray(data) ? data : []
      })
      .catch(() => {
        categories.value = []
      }),
  ])
})

watch(categoryFilter, () => {
  pinnedProviderId.value = null
})

const providersWithDistance = computed((): Record<string, unknown>[] => {
  const list = providerStore.providers as Record<string, unknown>[]
  const lat = userLat.value
  const lng = userLng.value
  if (lat == null || lng == null) {
    return list.map((p) => ({ ...p })) as Record<string, unknown>[]
  }
  return list
    .map((p) => {
      const plat = p.latitude
      const plng = p.longitude
      if (typeof plat === "number" && typeof plng === "number") {
        return {
          ...p,
          distance_km: haversine(lat, lng, plat, plng),
        } as Record<string, unknown>
      }
      return { ...p, distance_km: undefined } as Record<string, unknown>
    })
    .sort((a, b) => {
      const da = typeof a.distance_km === "number" ? a.distance_km : 9999
      const db = typeof b.distance_km === "number" ? b.distance_km : 9999
      return da - db
    })
})

const categoryFilteredProviders = computed((): Record<string, unknown>[] => {
  const list = providersWithDistance.value
  const idStr = categoryFilter.value
  if (!idStr) return list
  const id = parseInt(idStr, 10)
  if (!Number.isFinite(id)) return list
  const cat = categories.value.find((c) => c.id === id)
  if (!cat) return list
  return list.filter((p) => providerHasCategory(p, cat.name))
})

const suggestions = computed(() => {
  const q = searchDraft.value.trim()
  if (!q || providerStore.loading) return []
  const list = categoryFilteredProviders.value
  return list
    .map((p) => ({ p, score: scoreProviderQuery(q, p) }))
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score
      const da = typeof a.p.distance_km === "number" ? a.p.distance_km : 9999
      const db = typeof b.p.distance_km === "number" ? b.p.distance_km : 9999
      return da - db
    })
    .slice(0, SUGGESTION_LIMIT)
    .map((x) => x.p)
})

const showSuggestionDropdown = computed(
  () =>
    inputFocused.value &&
    suggestionsOpen.value &&
    searchDraft.value.trim().length > 0 &&
    suggestions.value.length > 0
)

watch(suggestions, () => {
  highlightIndex.value = 0
})

const filteredProviders = computed(() => {
  if (pinnedProviderId.value != null) {
    const id = pinnedProviderId.value
    const found = providersWithDistance.value.find((p) => Number(p.id) === id)
    return found ? [found] : []
  }

  const list = providersWithDistance.value
  const q = activeSearchQuery.value

  if (!q) {
    return list
  }

  const scored = list
    .map((p) => ({
      p,
      score: scoreProviderQuery(q, p),
    }))
    .filter((x) => x.score >= SEARCH_MATCH_THRESHOLD)
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score
      const da = typeof a.p.distance_km === "number" ? a.p.distance_km : 9999
      const db = typeof b.p.distance_km === "number" ? b.p.distance_km : 9999
      return da - db
    })

  return scored.map((x) => x.p)
})

const searchHadNoMatches = computed(
  () =>
    pinnedProviderId.value == null &&
    !!activeSearchQuery.value &&
    !providerStore.loading &&
    filteredProviders.value.length === 0 &&
    categoryFilteredProviders.value.length > 0
)

const categoryHasNoProviders = computed(
  () =>
    pinnedProviderId.value == null &&
    categoryFilter.value !== "" &&
    !providerStore.loading &&
    categoryFilteredProviders.value.length === 0
)
</script>

<template>
  <div class="providers-page">

    <form class="search-bar" @submit.prevent="runSearch">
      <label class="category-field">
        <span class="category-label">Category</span>
        <select
          v-model="categoryFilter"
          class="category-select"
          aria-label="Filter by category"
        >
          <option value="">All categories</option>
          <option v-for="c in categories" :key="c.id" :value="String(c.id)">
            {{ c.name }}
          </option>
        </select>
      </label>

      <div class="search-combo">
        <div class="search-input-wrap">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <input
            v-model="searchDraft"
            type="search"
            placeholder="Search category, services, shop, address…"
            autocomplete="off"
            enterkeyhint="search"
            role="combobox"
            :aria-expanded="showSuggestionDropdown"
            aria-autocomplete="list"
            aria-controls="provider-suggest-list"
            @focus="onSearchFocus"
            @blur="onSearchBlur"
            @input="onSearchInput"
            @keydown="onSearchKeydown"
          />
        </div>

        <ul
          v-show="showSuggestionDropdown"
          id="provider-suggest-list"
          class="suggest-dropdown"
          role="listbox"
          @mousedown.prevent
        >
          <li
            v-for="(p, i) in suggestions"
            :key="String(p.id)"
            role="option"
            :aria-selected="i === highlightIndex"
            class="suggest-item"
            :class="{ active: i === highlightIndex }"
            @mousedown.prevent="selectSuggestion(p)"
          >
            <div class="suggest-title">{{ p.shop_name }}</div>
            <div class="suggest-loc">{{ locationLine(p) }}</div>
            <div v-if="categoryLabel(p)" class="suggest-cat">{{ categoryLabel(p) }}</div>
          </li>
        </ul>
      </div>

      <button type="submit" class="search-btn">
        Search
      </button>

      <button type="button" class="location-btn" @click="useMyLocation">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="3" />
          <path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" />
        </svg>
        Use My Location
      </button>
    </form>

    <p v-if="categoryHasNoProviders" class="search-empty search-empty--muted" role="status">
      No providers in this category yet. Try another category or
      <button type="button" class="link-clear" @click="clearSearch">clear filters</button>.
    </p>

    <p v-else-if="searchHadNoMatches" class="search-empty" role="status">
      No close matches for “{{ activeSearchQuery }}”. Try different keywords or clear filters.
      <button type="button" class="link-clear" @click="clearSearch">Clear search</button>
    </p>

    <div v-if="providerStore.loading" class="map-loading">Loading providers…</div>

    <ProviderMap
      v-else
      :providers="filteredProviders"
      :userLat="userLat"
      :userLng="userLng"
    />

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap');

:global(html),
:global(body),
:global(#app) {
  margin: 0;
  padding: 0;
  height: 100%;
  background: #0e0c1a;
}

.providers-page {
  position: relative;
  height: 100vh;
  flex: 1;
  background: #0e0c1a;
  font-family: 'DM Sans', sans-serif;
  overflow: hidden;
}

.search-bar {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: min(760px, calc(100% - 40px));
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: flex-end;
}

.category-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: min(160px, 100%);
}

.category-label {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.category-select {
  min-width: 140px;
  padding: 12px 32px 12px 14px;
  background: rgba(14, 12, 26, 0.88);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  backdrop-filter: blur(16px);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.45)' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}
.category-select:focus {
  border-color: rgba(167, 139, 250, 0.45);
}
.category-select option {
  background: #13111f;
  color: #fff;
}

.search-combo {
  flex: 1;
  min-width: 140px;
  position: relative;
}

.search-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.search-input-wrap input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  background: rgba(14, 12, 26, 0.88);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  outline: none;
  backdrop-filter: blur(16px);
}

.search-input-wrap input:focus {
  border-color: rgba(167, 139, 250, 0.45);
}

.suggest-dropdown {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 6px);
  margin: 0;
  padding: 6px;
  list-style: none;
  max-height: min(320px, 42vh);
  overflow-y: auto;
  background: rgba(18, 16, 30, 0.97);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(16px);
  z-index: 1002;
}

.suggest-item {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.12s;
}
.suggest-item:hover,
.suggest-item.active {
  background: rgba(167, 139, 250, 0.12);
}

.suggest-title {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 4px;
  line-height: 1.3;
}

.suggest-loc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.45);
  line-height: 1.35;
}

.suggest-cat {
  margin-top: 6px;
  font-size: 11px;
  color: rgba(167, 139, 250, 0.85);
  letter-spacing: 0.02em;
}

.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 18px;
  background: rgba(255, 255, 255, 0.08);
  border: 0.5px solid rgba(255, 255, 255, 0.14);
  border-radius: 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s, border-color 0.15s;
}
.search-btn:hover {
  background: rgba(167, 139, 250, 0.15);
  border-color: rgba(167, 139, 250, 0.35);
}

.location-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.search-empty {
  position: absolute;
  top: 88px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  width: min(520px, calc(100% - 48px));
  margin: 0;
  padding: 10px 14px;
  font-size: 13px;
  line-height: 1.45;
  color: rgba(255, 255, 255, 0.75);
  background: rgba(14, 12, 26, 0.92);
  border: 0.5px solid rgba(248, 113, 113, 0.25);
  border-radius: 12px;
  backdrop-filter: blur(12px);
}

.link-clear {
  display: inline;
  margin-left: 8px;
  padding: 0;
  border: none;
  background: none;
  color: #a78bfa;
  font: inherit;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
}
.link-clear:hover {
  color: #c4b5fd;
}

.search-empty--muted {
  border-color: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.55);
}

.map-loading {
  position: absolute;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0e0c1a;
  color: rgba(255, 255, 255, 0.45);
  font-size: 14px;
}

@media (max-width: 640px) {
  .search-bar {
    flex-direction: column;
  }
  .search-btn,
  .location-btn {
    justify-content: center;
  }
  .search-empty {
    top: auto;
    bottom: 140px;
  }
}
</style>
