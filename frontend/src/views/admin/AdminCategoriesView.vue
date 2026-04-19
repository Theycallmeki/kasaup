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

<style scoped src="../../styles/admin/AdminCategoriesView.css"></style>