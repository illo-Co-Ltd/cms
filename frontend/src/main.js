import { createApp } from 'vue'
import App from './App.vue'
import router from '@/routes/routes.js'

import 'sweetalert2/dist/sweetalert2.min.css';

const app = createApp(App)
app.use(router)
app.mount('#app')
