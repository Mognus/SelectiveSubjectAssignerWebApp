import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SubjectsView from '../views/SubjectsView.vue'
import { useAuthStore } from '../stores/authStore'

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
            component: LoginView
        },
        {
            path: '/subjects',
            name: 'subjects',
            component: SubjectsView,
            meta: { requiresAuth: true }
        }
    ]
})

router.beforeEach(async (to, _, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth) {
        try {
            await authStore.refreshAccessToken()
        } catch {
            authStore.logout()
            next('/login')
            return;
        }
    }

    if (!authStore.user && authStore.accessToken) {
        try {
            await authStore.fetchUser(authStore.user?.id ?? 1)
        } catch {
            authStore.logout()
            next('/login')
            return;
        }
    }

    next();
})

export default router;
