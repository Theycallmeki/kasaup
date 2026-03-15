<script setup lang="ts">
import { onMounted } from "vue"
import { useCategoryStore } from "../../stores/categoryStore"

const categoryStore = useCategoryStore()

onMounted(() => {
  categoryStore.fetchCategories()
})
</script>

<template>

<div>

  <h2>Categories</h2>

  <div
    v-for="category in categoryStore.categories"
    :key="category.id"
  >
    {{ category.name }}
  </div>

</div>

</template>