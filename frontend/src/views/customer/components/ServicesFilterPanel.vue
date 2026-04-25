<script setup lang="ts">
import { computed } from "vue"

type SortOption = "price_asc" | "price_desc" | "duration"

const props = defineProps<{
  categories: any[]
  tempActiveCat: number | "all"
  tempSort: SortOption
  tempMinPrice: number | null
  tempMaxPrice: number | null
  tempMinRating: number
  tempMaxDistance: number | null
  tempUseLocation: boolean
  locLoading: boolean
}>()

const emit = defineEmits<{
  "update:tempActiveCat": [v: number | "all"]
  "update:tempSort": [v: SortOption]
  "update:tempMinPrice": [v: number | null]
  "update:tempMaxPrice": [v: number | null]
  "update:tempMinRating": [v: number]
  "update:tempMaxDistance": [v: number | null]
  clear: []
  cancel: []
  apply: []
  toggleLocation: []
}>()

const activeCatModel = computed({
  get: () => props.tempActiveCat,
  set: (v: number | "all") => emit("update:tempActiveCat", v),
})
const sortModel = computed({
  get: () => props.tempSort,
  set: (v: SortOption) => emit("update:tempSort", v),
})
const minPriceModel = computed({
  get: () => props.tempMinPrice,
  set: (v: number | null) => emit("update:tempMinPrice", v),
})
const maxPriceModel = computed({
  get: () => props.tempMaxPrice,
  set: (v: number | null) => emit("update:tempMaxPrice", v),
})
const minRatingModel = computed({
  get: () => props.tempMinRating,
  set: (v: number) => emit("update:tempMinRating", v),
})
const maxDistanceModel = computed({
  get: () => props.tempMaxDistance,
  set: (v: number | null) => emit("update:tempMaxDistance", v),
})
</script>

<template>
  <div class="filter-panel">
    <div class="fp-sections">
      <div class="filter-group">
        <h4>Category</h4>
        <div class="filter-pills">
          <button class="fp" :class="{ active: activeCatModel === 'all' }" @click="activeCatModel = 'all'">
            All Categories
          </button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="fp"
            :class="{ active: activeCatModel === cat.id }"
            @click="activeCatModel = cat.id"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>

      <div class="filter-group">
        <h4>Sort By</h4>
        <div class="filter-pills">
          <button class="fp" :class="{ active: sortModel === 'price_asc' }" @click="sortModel = 'price_asc'">
            Price: Low to High
          </button>
          <button class="fp" :class="{ active: sortModel === 'price_desc' }" @click="sortModel = 'price_desc'">
            Price: High to Low
          </button>
          <button class="fp" :class="{ active: sortModel === 'duration' }" @click="sortModel = 'duration'">
            Duration
          </button>
        </div>
      </div>

      <div class="filter-group">
        <h4>Price Range</h4>
        <div class="filter-inputs">
          <div class="input-with-symbol">
            <span>PHP</span>
            <input v-model.number="minPriceModel" type="number" placeholder="Min" />
          </div>
          <div class="input-divider">-</div>
          <div class="input-with-symbol">
            <span>PHP</span>
            <input v-model.number="maxPriceModel" type="number" placeholder="Max" />
          </div>
        </div>
      </div>

      <div class="filter-group">
        <h4>Minimum Rating</h4>
        <div class="filter-pills">
          <button class="fp" :class="{ active: minRatingModel === 0 }" @click="minRatingModel = 0">
            Any Rating
          </button>
          <button
            v-for="r in [5, 4, 3, 2]"
            :key="r"
            class="fp"
            :class="{ active: minRatingModel === r }"
            @click="minRatingModel = r"
          >
            {{ r }}* & Up
          </button>
        </div>
      </div>

      <div class="filter-group">
        <div class="fg-head">
          <h4>Distance Range</h4>
          <button
            class="toggle-switch"
            :class="{ on: tempUseLocation, loading: locLoading }"
            type="button"
            :disabled="locLoading"
            @click="emit('toggleLocation')"
          >
            <span class="switch-ball"></span>
          </button>
        </div>

        <div v-if="tempUseLocation" class="filter-pills">
          <button class="fp" :class="{ active: maxDistanceModel === null }" @click="maxDistanceModel = null">
            Anywhere
          </button>
          <button class="fp" :class="{ active: maxDistanceModel === 5 }" @click="maxDistanceModel = 5">5km</button>
          <button class="fp" :class="{ active: maxDistanceModel === 10 }" @click="maxDistanceModel = 10">
            10km
          </button>
          <button class="fp" :class="{ active: maxDistanceModel === 25 }" @click="maxDistanceModel = 25">
            25km
          </button>
          <div class="custom-dist-input">
            <input v-model.number="maxDistanceModel" type="number" placeholder="Custom" class="cd-input" />
            <span class="unit">km</span>
          </div>
        </div>
        <div v-else class="loc-off-msg">
          {{ locLoading ? "Getting your location..." : "Turn on to find services near you." }}
        </div>
      </div>
    </div>

    <div class="fp-actions">
      <button class="f-btn f-clear" @click="emit('clear')">Clear All</button>
      <button class="f-btn f-cancel" @click="emit('cancel')">Cancel</button>
      <button class="f-btn f-apply" @click="emit('apply')">Apply Filters</button>
    </div>
  </div>
</template>

<style scoped>
.filter-panel {
  width: 100%;
  background: #181628;
  border: 1px solid rgba(167, 139, 250, 0.2);
  border-radius: 16px;
  padding: 24px;
  margin-top: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.fp-sections {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 32px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-group h4 {
  margin: 0;
  font-family: "Sora", sans-serif;
  font-size: 0.95rem;
  color: #fff;
}

.fg-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}

.filter-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.fp {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  padding: 8px 16px;
  color: rgba(255, 255, 255, 0.7);
  font-family: "DM Sans", sans-serif;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  height: 38px;
  display: flex;
  align-items: center;
}

.fp:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.fp.active {
  background: #a78bfa;
  border-color: #a78bfa;
  color: #110e1b;
  font-weight: 600;
}

.filter-inputs {
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-with-symbol {
  position: relative;
  flex: 1;
}

.input-with-symbol span {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.7rem;
  pointer-events: none;
}

.input-with-symbol input {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 10px 10px 44px;
  color: #fff;
  font-family: "DM Sans", sans-serif;
  font-size: 0.9rem;
  outline: none;
  transition: all 0.2s;
}

.input-divider {
  color: rgba(255, 255, 255, 0.2);
}

.toggle-switch {
  width: 44px;
  height: 22px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 100px;
  position: relative;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.toggle-switch.on {
  background: #a78bfa;
}

.switch-ball {
  width: 14px;
  height: 14px;
  background: #fff;
  border-radius: 50%;
  position: absolute;
  top: 4px;
  left: 4px;
  transition: transform 0.3s;
}

.toggle-switch.on .switch-ball {
  transform: translateX(22px);
}

.toggle-switch.loading {
  opacity: 0.7;
  cursor: wait;
}

.custom-dist-input {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 100px;
  padding: 0 12px;
  height: 38px;
}

.cd-input {
  background: transparent;
  border: none;
  color: #fff;
  font-family: inherit;
  font-size: 0.85rem;
  width: 60px;
  outline: none;
  text-align: center;
}

.unit {
  font-size: 0.75rem;
  font-weight: 700;
  color: #a78bfa;
  margin-left: 2px;
}

.loc-off-msg {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.3);
  font-style: italic;
  padding: 4px 0;
}

.fp-actions {
  display: flex;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px dashed rgba(255, 255, 255, 0.1);
}

.f-btn {
  flex: 1;
  font-family: "DM Sans", sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.f-clear {
  background: transparent;
  border: 1px solid rgba(248, 113, 113, 0.2);
  color: rgba(248, 113, 113, 0.7);
}

.f-cancel {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
}

.f-apply {
  background: #a78bfa;
  border: none;
  color: #110e1b;
}

@media (max-width: 640px) {
  .filter-panel {
    border-radius: 16px;
    padding: 20px;
  }

  .fp-sections {
    display: flex;
    flex-direction: column;
    gap: 28px;
  }
}

/* Hide number input spinners */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
