import './styles/main.css'

import { createApp } from 'vue'
import { pinia } from './stores'
import { useSettingsStore } from './stores'

import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)

const appInstance = app.mount('#app')

// Initialize settings store after mounting
const settingsStore = useSettingsStore()
settingsStore.initialize()
