import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "../views/LoginView.vue";
import SubjectsView from '../views/SubjectsView.vue';
import {useAuthStore} from "../stores/authStore.ts";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
        },
        {
            path: '/subjects',
            name: 'subjects',
            component: SubjectsView,
            meta: { requiresAuth: true }
        },
    ],
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    if (from)
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})

export default router
