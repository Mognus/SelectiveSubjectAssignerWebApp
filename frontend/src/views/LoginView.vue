<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import Toast from 'primevue/toast';

const authStore = useAuthStore()
const router = useRouter()
const toast = useToast()

const password = ref('')

const handleLogin = async () => {
  try {
    await authStore.login(password.value)
    toast.add({ severity: 'success', summary: 'Erfolg', detail: 'Login erfolgreich', life: 10000 })
    await router.push('/')
  } catch (error) {
    console.error(error);
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Login fehlgeschlagen', life: 10000 })
  }
}
</script>

<template>
  <Toast />
  <form class="form" @submit.prevent="handleLogin">
    <span class="input-span">
      <label for="password" class="label">Passwort</label>
      <input type="password" v-model="password" name="password" id="password" required />
    </span>
    <span class="span"></span>
    <input class="submit" type="submit" value="Log in" />
  </form>
</template>

<style scoped>
.form {
  --bg-light: #efefef;
  --bg-dark: #707070;
  --clr: #58bc82;
  --clr-alpha: #9c9c9c60;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 300px;
}

.form .input-span {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form input[type="text"],
.form input[type="password"] {
  border-radius: 0.5rem;
  padding: 1rem 0.75rem;
  width: 100%;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--clr-alpha);
  outline: 2px solid var(--bg-dark);
}

.form input[type="text"]:focus,
.form input[type="password"]:focus {
  outline: 2px solid var(--clr);
}

.label {
  align-self: flex-start;
  color: var(--clr);
  font-weight: 600;
}

.form .submit {
  padding: 1rem 0.75rem;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 3rem;
  background-color: var(--bg-dark);
  color: var(--bg-light);
  border: none;
  cursor: pointer;
  transition: all 300ms;
  font-weight: 600;
  font-size: 0.9rem;
}

.form .submit:hover {
  background-color: var(--clr);
  color: var(--bg-dark);
}

.span {
  text-decoration: none;
  color: var(--bg-dark);
}

.span a {
  color: var(--clr);
}
</style>
