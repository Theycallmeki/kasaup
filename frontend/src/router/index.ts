import { createRouter, createWebHistory } from "vue-router"

import LoginView from "../views/auth/LoginView.vue"
import RegisterView from "../views/auth/RegisterView.vue"
import ProviderListView from "../views/ProviderListView.vue"
import ProviderProfileView from "../views/ProviderProfileView.vue"
import MyAppointmentsView from "../views/MyAppointmentsView.vue"
import AuthSelectView from "../views/auth/AuthSelectView.vue"

import { useAuthStore } from "../stores/authStore"

const routes = [
  {
    path: "/",
    redirect: "/auth"
  },
  {
    path: "/auth",
    name: "auth",
    component: AuthSelectView
  },
  {
    path: "/login",
    name: "login",
    component: LoginView
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView
  },
  {
    path: "/providers",
    name: "providers",
    component: ProviderListView,
    meta: { requiresAuth: true }
  },
  {
    path: "/providers/:id",
    name: "providerProfile",
    component: ProviderProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: "/appointments",
    name: "appointments",
    component: MyAppointmentsView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {

  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.user) {

    try {
      await auth.fetchUser()
    } catch {
      return { path: "/login" }
    }

    if (!auth.user) {
      return { path: "/login" }
    }

  }

})

export default router
