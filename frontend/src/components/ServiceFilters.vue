<script setup lang="ts">
defineProps<{
  categories: any[]
  searching: boolean
}>()

const emit = defineEmits<{
  "update:query":     [v: string]
  "update:activeCat": [v: number | "all"]
  "update:sort":      [v: string]
}>()
</script>

<template>
  <div class="filters">

    <!-- Search + Sort -->
    <div class="row">
      <div class="srch">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
        </svg>
        <input
          placeholder="Search services, providers…"
          @input="emit('update:query', ($event.target as HTMLInputElement).value)"
        />
        <span v-if="searching" class="spin" />
      </div>
      <select class="sel" @change="emit('update:sort', ($event.target as HTMLSelectElement).value)">
        <option value="price_asc">Price ↑</option>
        <option value="price_desc">Price ↓</option>
        <option value="duration">Duration</option>
      </select>
    </div>

    <!-- Category pills -->
    <div class="cats" v-if="categories.length">
      <button class="cp active" @click="emit('update:activeCat', 'all')">✦ All</button>
      <button
        v-for="cat in categories" :key="cat.id"
        class="cp"
        @click="emit('update:activeCat', cat.id)"
      >{{ cat.name }}</button>
    </div>

  </div>
</template>

<style scoped>
.filters { display:flex; flex-direction:column; gap:14px; margin-bottom:20px; }

.row { display:flex; gap:10px; flex-wrap:wrap; }

.srch { position:relative; flex:1; min-width:180px; }
.srch svg { position:absolute; left:12px; top:50%; transform:translateY(-50%); width:15px; height:15px; color:rgba(255,255,255,.25); pointer-events:none; }
.srch input { width:100%; box-sizing:border-box; background:rgba(255,255,255,.04); border:0.5px solid rgba(255,255,255,.1); border-radius:10px; padding:10px 36px; color:#fff; font-family:'DM Sans',sans-serif; font-size:.875rem; outline:none; transition:border-color .15s; }
.srch input::placeholder { color:rgba(255,255,255,.22); }
.srch input:focus { border-color:rgba(130,90,255,.45); }

.spin { display:inline-block; width:13px; height:13px; border:2px solid rgba(255,255,255,.1); border-top-color:#a78bfa; border-radius:50%; animation:sp .6s linear infinite; position:absolute; right:12px; top:50%; transform:translateY(-50%); }
@keyframes sp { to { transform:translateY(-50%) rotate(360deg) } }

.sel { background:rgba(255,255,255,.04); border:0.5px solid rgba(255,255,255,.1); border-radius:10px; padding:10px 14px; color:#fff; font-family:'DM Sans',sans-serif; font-size:.875rem; outline:none; cursor:pointer; }
.sel option { background:#1a1730; }

.cats { display:flex; gap:8px; flex-wrap:wrap; }
.cp { padding:6px 14px; border-radius:100px; border:0.5px solid rgba(255,255,255,.1); background:rgba(255,255,255,.03); color:rgba(255,255,255,.45); font-family:'DM Sans',sans-serif; font-size:.82rem; font-weight:500; cursor:pointer; transition:all .15s; white-space:nowrap; }
.cp:hover { background:rgba(255,255,255,.07); color:#fff; }
.cp.active { background:rgba(99,60,220,.2); border-color:rgba(130,90,255,.4); color:#c4b5fd; }
</style>