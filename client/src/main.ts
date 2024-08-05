/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import router from './router'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import vuetify from './plugins/vuetify'
//import Toast from 'vue-toastification';

const app = createApp(App)

registerPlugins(app)

app.use(router).use(vuetify).mount('#app')
