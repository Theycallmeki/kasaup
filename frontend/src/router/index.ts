import { createRouter, createWebHistory } from "vue-router"

import HomeView from "../views/customer/HomeView.vue"
import LoginView from "../views/auth/LoginView.vue"
import RegisterView from "../views/auth/RegisterView.vue"
import AuthSelectView from "../views/auth/AuthSelectView.vue"

import ProviderListView from "../views/customer/ProviderListView.vue"
import ProviderProfileView from "../views/customer/ProviderProfileView.vue"
import MyAppointmentsView from "../views/customer/MyAppointmentsView.vue"

import ProviderDashboardView from "../views/provider/ProviderDashboardView.vue"
import ProviderServicesView from "../views/provider/ProviderServicesView.vue"
import ProviderAvailabilityView from "../views/provider/ProviderAvailabilityView.vue"
import ProviderAppointmentsView from "../views/provider/ProviderAppointmentsView.vue"
import CreateServiceView from "../views/provider/CreateServiceView.vue"
import CreateProviderProfileView from "../views/provider/CreateProviderProfileView.vue"

import AdminDashboardView from "../views/admin/AdminDashboardView.vue"
import AdminCategoriesView from "../views/admin/AdminCategoriesView.vue"
import AdminUsersView from "../views/admin/AdminUsersView.vue"
import AdminProvidersView from "../views/admin/AdminProvidersView.vue"

import { useAuthStore } from "../stores/authStore"
import api from "../services/api"

const routes = [

  {
    path: "/",
    name: "home",
    component: HomeView
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
    meta: { requiresAuth: true, roles: ["customer"] }
  },

  {
    path: "/providers/:id",
    name: "providerProfile",
    component: ProviderProfileView,
    meta: { requiresAuth: true, roles: ["customer"] }
  },

  {
    path: "/appointments",
    name: "appointments",
    component: MyAppointmentsView,
    meta: { requiresAuth: true, roles: ["customer"] }
  },

  {
    path: "/provider/create-profile",
    name: "createProviderProfile",
    component: CreateProviderProfileView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/provider/dashboard",
    name: "providerDashboard",
    component: ProviderDashboardView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/provider/services",
    name: "providerServices",
    component: ProviderServicesView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/provider/services/create",
    name: "createService",
    component: CreateServiceView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/provider/availability",
    name: "providerAvailability",
    component: ProviderAvailabilityView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/provider/appointments",
    name: "providerAppointments",
    component: ProviderAppointmentsView,
    meta: { requiresAuth: true, roles: ["provider"] }
  },

  {
    path: "/admin/dashboard",
    name: "adminDashboard",
    component: AdminDashboardView,
    meta: { requiresAuth: true, roles: ["admin"] }
  },

  {
    path: "/admin/categories",
    name: "adminCategories",
    component: AdminCategoriesView,
    meta: { requiresAuth: true, roles: ["admin"] }
  },

  {
    path: "/admin/users",
    name: "adminUsers",
    component: AdminUsersView,
    meta: { requiresAuth: true, roles: ["admin"] }
  },

  {
    path: "/admin/providers",
    name: "adminProviders",
    component: AdminProvidersView,
    meta: { requiresAuth: true, roles: ["admin"] }
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {

  const auth = useAuthStore()

  if (to.meta.requiresAuth) {

    if (!auth.user) {
      try {
        await auth.fetchUser()
      } catch {
        return { path: "/login" }
      }
    }

    if (!auth.user) {
      return { path: "/login" }
    }

    const allowedRoles = to.meta.roles as string[]

    if (allowedRoles && !allowedRoles.includes(auth.user.role)) {

      if (auth.user.role === "provider") {
        return { path: "/provider/dashboard" }
      }

      if (auth.user.role === "admin") {
        return { path: "/admin/dashboard" }
      }

      if (auth.user.role === "customer") {
        return { path: "/providers" }
      }

    }

    if (auth.user.role === "provider") {

      try {

        const res = await api.get("/providers")

        const provider = res.data.find(
          (p:any) => p.owner_id === auth.user.id
        )

        if (!provider && to.path !== "/provider/create-profile") {
          return { path: "/provider/create-profile" }
        }

        if (provider && to.path === "/provider/create-profile") {
          return { path: "/provider/dashboard" }
        }

      } catch {}

    }

  }

})

export default router