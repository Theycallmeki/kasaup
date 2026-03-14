import { createRouter, createWebHistory } from "vue-router"

import HomeView from "../views/HomeView.vue"
import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import ProviderListView from "../views/ProviderListView.vue"
import ProviderProfileView from "../views/ProviderProfileView.vue"
import MyAppointmentsView from "../views/MyAppointmentsView.vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView
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
    component: ProviderListView
  },
  {
    path: "/providers/:id",
    name: "providerProfile",
    component: ProviderProfileView
  },
  {
    path: "/appointments",
    name: "appointments",
    component: MyAppointmentsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router