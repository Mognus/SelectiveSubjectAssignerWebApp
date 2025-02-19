import { defineStore } from 'pinia';
import axios from '../utils/api';
import type { AxiosError } from 'axios';
import router from '../router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: sessionStorage.getItem('accessToken') || '',
        user: sessionStorage.getItem('user') ? JSON.parse(sessionStorage.getItem('user') as string) : null,
        isLoggingOut: false
    }),
    getters: {
        isAuthenticated: (state) => Boolean(state.accessToken && state.user)
    },
    actions: {
        async login(password: string) {
            try {
                const response = await axios.post('/get-token/', { password });

                if (response.data.access) {
                    this.setAccessToken(response.data.access);
                } else {
                    throw new Error('Token nicht erhalten');
                }

                await this.fetchUser(response.data.user_id);
            } catch (error) {
                throw error;
            }
        },

        async fetchUser(userId: number) {
            if (this.isLoggingOut || !this.accessToken) {
                this.logout();
                return;
            }
            try {
                const response = await axios.get(`/users/${userId}/`, {
                    headers: { Authorization: `Bearer ${this.accessToken}` }
                });
                this.user = response.data;
                sessionStorage.setItem('user', JSON.stringify(this.user));
            } catch (error) {
                const axiosError = error as AxiosError;
                if (axiosError.response?.status === 401) {
                    await this.refreshAccessToken();
                } else {
                    this.logout();
                }
            }
        },

        async refreshAccessToken() {
            if (this.isLoggingOut || !this.accessToken) {
                this.logout();
                return;
            }
            try {
                const response = await axios.post('/verify-token/', { token: this.accessToken });
                if (response.status !== 200) {
                    this.logout();
                } else {
                    this.setAccessToken(this.accessToken);
                }
            } catch {
                this.logout();
            }
        },

        setAccessToken(token: string) {
            this.accessToken = token;
            sessionStorage.setItem('accessToken', token);
        },

        logout() {
            this.isLoggingOut = true;
            this.accessToken = '';
            this.user = null;
            sessionStorage.removeItem('accessToken');
            sessionStorage.removeItem('user');
            router.push('/login');
        }
    }
});
