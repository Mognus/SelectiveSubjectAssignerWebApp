import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import {createPinia} from "pinia";
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import ToastService from 'primevue/toastservice';


const pinia = createPinia();
const app = createApp(App);

app.use(pinia)
    .use(router)
    .use(ToastService)
    .use(PrimeVue, {
        theme: {
            preset: Aura
        }
    })
    .mount('#app')
