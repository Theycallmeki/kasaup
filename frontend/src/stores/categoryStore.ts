import { defineStore } from "pinia"
import { getCategories } from "../services/categories"

export const useCategoryStore = defineStore("categories", {

  state: () => ({
    categories: [] as any[]
  }),

  actions: {

    async fetchCategories() {
      this.categories = await getCategories()
    }

  }

})