import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'light'
    }
  })

import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)
app.use(vuetify);
app.use(VueAxios, axios)
app.mount('#app')