import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme: {
        dark: false,
        colors: {
          primary: '#235d3b',
          secondary: '#4c8b6c', // สีอ่อนกว่า
          accent: '#82b59e',    // สีอ่อนที่สุด
          background: '#f5f5f5'
        }
      }
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')