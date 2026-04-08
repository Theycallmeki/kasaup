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
import { useScroll } from "../../hooks/useScroll"
import { useLoading } from "../../hooks/useLoading"

const providerStore = useProviderStore()
const { startLoading, stopLoading } = useLoading()
const { scrollRef: suggestionScroll } = useScroll()

const userLat = ref<number | null>(null)
const userLng = ref<number | null>(null)

const searchDraft = ref("")
const activeSearchQuery = ref("")
const pinnedProviderId = ref<number | null>(null)

const suggestionsOpen = ref(false)
const highlightIndex = ref(0)
const inputFocused = ref(false)
const showFilters = ref(false)

const USER_LOCATION_KEY = "kasaup:user_location_v1"
const SUGGESTION_LIMIT = 8

const categories = ref<{ id: number; name: string }[]>([])
const categoryFilter = ref("")

function providerHasCategory(p: Record<string, unknown>, categoryName: string): boolean {
  const names = Array.isArray(p.category_names) ? (p.category_names as string[]) : []
  const t = normalizeText(categoryName)
  return names.some((n) => normalizeText(n) === t)
}

function persistUserLocation(lat: number, lng: number) {
  try {
    sessionStorage.setItem(USER_LOCATION_KEY, JSON.stringify({ lat, lng }))
  } catch { }
}

function restoreUserLocation() {
  try {
    const raw = sessionStorage.getItem(USER_LOCATION_KEY)
    if (!raw) return
    const parsed = JSON.parse(raw) as { lat?: unknown; lng?: unknown }
    if (typeof parsed.lat === "number" && typeof parsed.lng === "number") {
      userLat.value = parsed.lat
      userLng.value = parsed.lng
    }
  } catch { }
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
  if (!navigator.geolocation) return
  startLoading("Detecting your location...")
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLat.value = pos.coords.latitude
      userLng.value = pos.coords.longitude
      persistUserLocation(userLat.value, userLng.value)
      stopLoading()
    },
    () => { 
      stopLoading()
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
  showFilters.value = false
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
  showFilters.value = false
}

function onSearchFocus() {
  inputFocused.value = true
  if (searchDraft.value.trim().length > 0) suggestionsOpen.value = true
}

function onSearchBlur() {
  inputFocused.value = false
  window.setTimeout(() => { suggestionsOpen.value = false }, 180)
}

function onSearchInput() {
  pinnedProviderId.value = null
  highlightIndex.value = 0
  suggestionsOpen.value = searchDraft.value.trim().length > 0
}

function onSearchKeydown(e: KeyboardEvent) {
  const list = suggestions.value
  const open = showSuggestionDropdown.value

  if (e.key === "Escape") { suggestionsOpen.value = false; return }
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
  startLoading("Finding providers near you...")
  try {
    restoreUserLocation()
    await Promise.all([
      providerStore.fetchProviders(),
      getCategories({ limit: 500, offset: 0 })
        .then((data: { id: number; name: string }[]) => {
          categories.value = Array.isArray(data) ? data : []
        })
        .catch(() => { categories.value = [] }),
    ])
  } finally {
    stopLoading()
  }
})

watch(categoryFilter, () => { pinnedProviderId.value = null })

const providersWithDistance = computed((): Record<string, unknown>[] => {
  const list = providerStore.providers as Record<string, unknown>[]
  const lat = userLat.value
  const lng = userLng.value
  if (lat == null || lng == null) return list.map((p) => ({ ...p }))
  return list
    .map((p) => {
      const plat = p.latitude
      const plng = p.longitude
      if (typeof plat === "number" && typeof plng === "number") {
        return { ...p, distance_km: haversine(lat, lng, plat, plng) }
      }
      return { ...p, distance_km: undefined }
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

  return categoryFilteredProviders.value
    .map((p) => ({ p, score: scoreProviderQuery(q, p) }))
    .filter((x) => x.score >= SEARCH_MATCH_THRESHOLD)
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

watch(suggestions, () => { highlightIndex.value = 0 })

const filteredProviders = computed(() => {
  if (pinnedProviderId.value != null) {
    const id = pinnedProviderId.value
    const found = categoryFilteredProviders.value.find((p) => Number(p.id) === id)
    return found ? [found] : []
  }

  const list = categoryFilteredProviders.value
  const q = activeSearchQuery.value

  if (!q) return list

  return list
    .map((p) => ({ p, score: scoreProviderQuery(q, p) }))
    .filter((x) => x.score >= SEARCH_MATCH_THRESHOLD)
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score
      const da = typeof a.p.distance_km === "number" ? a.p.distance_km : 9999
      const db = typeof b.p.distance_km === "number" ? b.p.distance_km : 9999
      return da - db
    })
    .map((x) => x.p)
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

const activeFilterCount = computed(() => {
  let count = 0
  if (categoryFilter.value !== "") count++
  return count
})
</script>

<template>
  <div class="providers-page">

    <!-- Unified Search Bar -->
    <div class="search-bar-wrapper">
      <form class="search-bar" @submit.prevent="runSearch">

        <!-- Search Input with Dropdown Toggle (Mobile) -->
        <div class="search-input-section search-with-filter">
          <div class="search-input-wrap">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input v-model="searchDraft" type="search" placeholder="Search providers, services…" autocomplete="off"
              @focus="onSearchFocus" @blur="onSearchBlur" @input="onSearchInput" @keydown="onSearchKeydown" />
          </div>

          <!-- FILTER ICON (moved here) -->
          <button type="button" class="filter-toggle filter-toggle--mobile" @click.prevent="showFilters = !showFilters">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
          </button>

          <!-- Suggestion Dropdown -->
          <ul v-show="showSuggestionDropdown" class="suggest-dropdown" ref="suggestionScroll">
            <li v-for="(p, i) in suggestions" :key="String(p.id)" class="suggest-item"
              :class="{ active: i === highlightIndex }" @mousedown.prevent="selectSuggestion(p)">
              <div class="suggest-title">{{ p.shop_name }}</div>
              <div class="suggest-loc">{{ locationLine(p) }}</div>
              <div v-if="categoryLabel(p)" class="suggest-cat">{{ categoryLabel(p) }}</div>
            </li>
          </ul>
        </div>

        <!-- Filter Toggle Button (Mobile) / Category Dropdown (Desktop) -->
        <div class="filter-section">
          <select v-model="categoryFilter" class="category-select">
            <option value="">All Categories</option>
            <option v-for="c in categories" :key="c.id" :value="String(c.id)">
              {{ c.name }}
            </option>
          </select>
        </div>



        <!-- Action Buttons -->
        <div class="action-buttons">
          <button type="button" class="location-btn" @click="useMyLocation">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3" />
              <path
                d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" />
            </svg>
            <span class="btn-label">Use my location</span>
          </button>

          <button type="submit" class="search-btn">Search</button>
        </div>
      </form>

      <!-- Mobile Filter Dropdown Panel -->
      <div v-if="showFilters" class="mobile-filter-panel">
        <div class="filter-panel-content">
          <h3 class="filter-panel-title">Category</h3>
          <div class="filter-options">
            <button type="button" class="filter-option" :class="{ active: categoryFilter === '' }"
              @click="categoryFilter = ''; showFilters = false">
              All Categories
              <svg v-if="categoryFilter === ''" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
              </svg>
            </button>
            <button v-for="c in categories" :key="c.id" type="button" class="filter-option"
              :class="{ active: categoryFilter === String(c.id) }"
              @click="categoryFilter = String(c.id); showFilters = false">
              {{ c.name }}
              <svg v-if="categoryFilter === String(c.id)" width="16" height="16" viewBox="0 0 24 24"
                fill="currentColor">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
              </svg>
            </button>
          </div>
          <button v-if="categoryFilter !== ''" type="button" class="clear-filter-btn"
            @click="categoryFilter = ''; showFilters = false">
            Clear Filter
          </button>
        </div>
      </div>
    </div>

    <!-- Error/Empty States -->
    <p v-if="categoryHasNoProviders" class="search-empty search-empty--muted">
      No providers in this category yet.
      <button type="button" class="link-clear" @click="clearSearch">clear filters</button>
    </p>

    <p v-else-if="searchHadNoMatches" class="search-empty">
      No matches for "{{ activeSearchQuery }}"
      <button type="button" class="link-clear" @click="clearSearch">Clear search</button>
    </p>

    <!-- Map -->
    <div v-if="providerStore.loading" class="map-loading">Loading providers…</div>

    <ProviderMap v-else :providers="filteredProviders" :userLat="userLat" :userLng="userLng"
      :hide-zoom-controls="true" />

  </div>
</template>

<style scoped src="../../styles/customer/ProviderListView.css"></style>