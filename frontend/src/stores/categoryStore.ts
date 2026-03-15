import { defineStore } from "pinia"
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory
} from "../services/categories"

export const useCategoryStore = defineStore("categories", {

  state: () => ({
    categories: [] as any[],
    loading: false
  }),

  actions: {

    async fetchCategories() {

      this.loading = true

      try {
        this.categories = await getCategories()
      } finally {
        this.loading = false
      }

    },

    async addCategory(data: { name: string }) {

      const res = await createCategory(data)

      await this.fetchCategories()

      return res

    },

    async editCategory(id: number, data: { name: string }) {

      const res = await updateCategory(id, data)

      await this.fetchCategories()

      return res

    },

    async removeCategory(id: number) {

      const res = await deleteCategory(id)

      await this.fetchCategories()

      return res

    }

  }

})