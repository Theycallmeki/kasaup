import { defineStore } from "pinia"
import {
  getCategories,
  createCategory,
  updateCategory,
  deleteCategory
} from "../services/categories"

export const useCategoryStore = defineStore("categories", {

  state: () => ({
    categories: [] as any[]
  }),

  actions: {

    async fetchCategories() {
      this.categories = await getCategories()
    },

    async addCategory(data: any) {
      return await createCategory(data)
    },

    async editCategory(id: number, data: any) {
      return await updateCategory(id, data)
    },

    async removeCategory(id: number) {
      return await deleteCategory(id)
    }

  }

})