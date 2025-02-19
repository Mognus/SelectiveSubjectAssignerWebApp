import axios, { AxiosError } from 'axios';
import { useAuthStore } from '../stores/authStore';

const api = axios.create({
    baseURL: 'http://localhost/api/',
    headers: { 'Content-Type': 'application/json' }
});

let refreshPromise: Promise<void> | null = null;

async function handleUnauthorized(error: AxiosError, originalRequest: any) {
    const authStore = useAuthStore();

    if (!authStore.accessToken) {
        authStore.logout();
        return Promise.reject(error);
    }

    if (!refreshPromise) {
        refreshPromise = authStore.refreshAccessToken().finally(() => {
            refreshPromise = null;
        });
    }

    try {
        await refreshPromise;
        if (!authStore.accessToken) {
            return Promise.reject(error);
        }
        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`;
        return api(originalRequest);
    } catch {
        return Promise.reject(error);
    }
}

api.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore();
        if (authStore.accessToken && config.url !== '/get-token/') {
            config.headers.Authorization = `Bearer ${authStore.accessToken}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config;

        if (!originalRequest) return Promise.reject(error);

        if (error.response?.status === 401) {
            return handleUnauthorized(error, originalRequest);
        }

        return Promise.reject(error);
    }
);

export default api;
