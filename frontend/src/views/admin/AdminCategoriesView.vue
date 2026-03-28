<script setup lang="ts">
import { onMounted, ref } from "vue"
import { useCategoryStore } from "../../stores/categoryStore"

const categoryStore = useCategoryStore()

const newName = ref("")
const adding = ref(false)

const editingId = ref<number | null>(null)
const editingName = ref("")
const editingLoading = ref(false)

const deletingId = ref<number | null>(null)

onMounted(() => {
  categoryStore.fetchCategories()
})

const startAdd = () => {
  newName.value = ""
  adding.value = true
  editingId.value = null
}

const cancelAdd = () => {
  adding.value = false
  newName.value = ""
}

const submitAdd = async () => {
  const name = newName.value.trim()
  if (!name) return
  await categoryStore.addCategory({ name })
  adding.value = false
  newName.value = ""
}

const startEdit = (category: any) => {
  editingId.value = category.id
  editingName.value = category.name
  adding.value = false
}

const cancelEdit = () => {
  editingId.value = null
  editingName.value = ""
}

const submitEdit = async (id: number) => {
  const name = editingName.value.trim()
  if (!name) return
  editingLoading.value = true
  await categoryStore.editCategory(id, { name })
  editingLoading.value = false
  editingId.value = null
}

const confirmDelete = async (id: number) => {
  deletingId.value = id
}

const cancelDelete = () => {
  deletingId.value = null
}

const submitDelete = async (id: number) => {
  await categoryStore.removeCategory(id)
  deletingId.value = null
}
</script>

<template>
  <div class="page">

    <div class="page-header">
      <div>
        <div class="header-label">Admin</div>
        <h1 class="title">Categories</h1>
        <p class="hint">Manage the service categories available on the platform.</p>
      </div>
      <button class="add-btn" @click="startAdd">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Add Category
      </button>
    </div>

    <!-- Add row -->
    <div v-if="adding" class="add-row">
      <input
        v-model="newName"
        class="field"
        placeholder="Category name..."
        @keydown.enter="submitAdd"
        @keydown.esc="cancelAdd"
        autofocus
      />
      <button class="action-btn action-btn--save" @click="submitAdd">Save</button>
      <button class="action-btn action-btn--cancel" @click="cancelAdd">Cancel</button>
    </div>

    <!-- List -->
    <div class="list">

      <div v-if="categoryStore.loading" class="empty-state">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
          <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
        </svg>
        Loading...
      </div>

      <div v-else-if="!categoryStore.categories.length" class="empty-state">
        No categories yet. Add one above.
      </div>

      <div
        v-for="category in categoryStore.categories"
        :key="category.id"
        class="list-item"
      >
        <!-- Delete confirm overlay -->
        <div v-if="deletingId === category.id" class="delete-confirm">
          <span class="delete-confirm-text">Delete <strong>{{ category.name }}</strong>?</span>
          <button class="action-btn action-btn--danger" @click="submitDelete(category.id)">Delete</button>
          <button class="action-btn action-btn--cancel" @click="cancelDelete">Cancel</button>
        </div>

        <!-- Edit mode -->
        <template v-else-if="editingId === category.id">
          <div class="category-icon">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
          </div>
          <input
            v-model="editingName"
            class="field field--inline"
            @keydown.enter="submitEdit(category.id)"
            @keydown.esc="cancelEdit"
            autofocus
          />
          <div class="item-actions">
            <button class="action-btn action-btn--save" :disabled="editingLoading" @click="submitEdit(category.id)">
              <svg v-if="editingLoading" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
              Save
            </button>
            <button class="action-btn action-btn--cancel" @click="cancelEdit">Cancel</button>
          </div>
        </template>

        <!-- Default view -->
        <template v-else>
          <div class="category-icon">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
          </div>
          <span class="category-name">{{ category.name }}</span>
          <div class="item-actions">
            <button class="icon-btn" title="Edit" @click="startEdit(category)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="icon-btn icon-btn--danger" title="Delete" @click="confirmDelete(category.id)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                <path d="M10 11v6"/><path d="M14 11v6"/>
                <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
              </svg>
            </button>
          </div>
        </template>
      </div>

    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700&family=DM+Sans:wght@400;500&display=swap');

.page {
  min-height: 100vh;
  background: #0e0c1a;
  padding: 36px 32px;
  font-family: 'DM Sans', sans-serif;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.header-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(167, 139, 250, 0.6);
  margin-bottom: 6px;
}

.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 6px;
}

.hint {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  padding: 9px 16px;
  border-radius: 10px;
  background: rgba(124, 58, 237, 0.35);
  border: 1px solid rgba(124, 58, 237, 0.5);
  color: #fff;
  cursor: pointer;
  transition: all 0.15s ease;
}

.add-btn:hover {
  background: rgba(124, 58, 237, 0.5);
  transform: translateY(-1px);
}

.add-row {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  background: rgba(124, 58, 237, 0.08);
  border: 1px dashed rgba(167, 139, 250, 0.4);
  border-radius: 12px;
  padding: 12px;
  max-width: 600px;
}

.list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.list-item {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 14px;
  min-height: 140px;
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
  position: relative;
}

.list-item:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 30px rgba(0,0,0,0.4);
  border-color: rgba(167, 139, 250, 0.3);
}

.category-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(124, 58, 237, 0.2);
  border: 1px solid rgba(124, 58, 237, 0.3);
  color: #a78bfa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  transition: transform 0.2s;
}

.list-item:hover .category-icon {
  transform: scale(1.1);
}

.category-name {
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  line-height: 1.4;
  margin-bottom: auto;
}

.item-actions {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
  margin-top: 12px;
  opacity: 0;
  transform: translateY(6px);
  transition: all 0.2s ease;
}

.list-item:hover .item-actions {
  opacity: 1;
  transform: translateY(0);
}

.field {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 8px;
  color: #fff;
  flex: 1;
}

.field:focus {
  border-color: rgba(167, 139, 250, 0.5);
}

.action-btn {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
}

.action-btn--save {
  background: rgba(124, 58, 237, 0.4);
  color: #fff;
}

.action-btn--cancel {
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.6);
}

.action-btn--danger {
  background: rgba(248, 113, 113, 0.2);
  color: #f87171;
}

.icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
}

.icon-btn:hover {
  color: #a78bfa;
  background: rgba(167, 139, 250, 0.12);
}

.icon-btn--danger {
  color: rgba(248, 113, 113, 0.5);
}

.icon-btn--danger:hover {
  color: #f87171;
  background: rgba(248, 113, 113, 0.12);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  color: rgba(255,255,255,0.3);
  padding: 40px 0;
}

@media (max-width: 640px) {
  .page {
    padding: 24px 16px;
  }
}
</style>