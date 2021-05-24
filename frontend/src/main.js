import { createApp } from 'vue'
import App from './App.vue'
import router from '@/routes/routes.js'
import mitt from 'mitt'
import 'sweetalert2/dist/sweetalert2.min.css';


const emitter = mitt()

const app = createApp(App)
app.provide('emitter', emitter)
app.use(router)
app.mount('#app')
