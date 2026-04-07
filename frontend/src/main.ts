import { createApp } from "vue"
import { createPinia } from "pinia"
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Aura from '@primevue/themes/aura'
import App from "./App.vue"
import router from "./router"

import "leaflet/dist/leaflet.css"
import "primeicons/primeicons.css"
import "./style.css"

const app = createApp(App)

const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: '.my-app-dark',
            cssLayer: false
        }
    }
})
app.use(ToastService)
app.use(ConfirmationService)

app.mount("#app")