<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Dropdown from 'primevue/dropdown';
import Card from 'primevue/card';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
import axios from '../utils/api';
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';
import Toast from 'primevue/toast';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const subjects = ref<{ subject_id: number; subject_name: string }[]>([]);
const firstChoice = ref<number | null>(null);
const secondChoice = ref<number | null>(null);
const thirdChoice = ref<number | null>(null);
const options = ref<{ label: string; value: number }[]>([]);

const fetchSubjects = async () => {
  try {
    const response = await axios.get('/subjects/', {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    });
    subjects.value = response.data;

    options.value = subjects.value.map((subject) => ({
      label: subject.subject_name,
      value: subject.subject_id
    }));
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Kurse konnten nicht geladen werden.', life: 3000 });
  }
};

const submitChoices = async () => {
  if (!authStore.accessToken || !authStore.user) {
    authStore.logout();
    router.push('/login');
    return;
  }

  try {
    await axios.post('/verify-token/', { token: authStore.accessToken });

    const requestData = {
      first_choice: firstChoice.value,
      second_choice: secondChoice.value,
      third_choice: thirdChoice.value
    };

    await axios.patch(`/users/${authStore.user.id}/`, requestData, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    });

    toast.add({ severity: 'success', summary: 'Gespeichert', detail: 'Deine Wünsche wurden gespeichert.', life: 3000 });

    setTimeout(() => {
      authStore.logout();
      router.push('/login');
    }, 3000);

  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Speichern fehlgeschlagen.', life: 3000 });
  }
};

onMounted(fetchSubjects);
</script>

<template>
  <div class="home">
    <Toast />
    <div class="container">
      <Card class="custom-card">
        <template #title>
          Wahlpflichtfach Manager
        </template>
        <template #content>
          <p class="description">
            Bitte wähle die Kurse aus, die du künftig besuchen möchtest.
          </p>

          <div class="select-group">
            <label for="first">1. Wunsch</label>
            <Dropdown v-model="firstChoice" :options="options" optionLabel="label" optionValue="value" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <div class="select-group">
            <label for="second">2. Wunsch</label>
            <Dropdown v-model="secondChoice" :options="options" optionLabel="label" optionValue="value" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <div class="select-group">
            <label for="third">3. Wunsch</label>
            <Dropdown v-model="thirdChoice" :options="options" optionLabel="label" optionValue="value" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <br>
          <Button label="Absenden" class="confirm-button" @click="submitChoices" />
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 75%;
}

.custom-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.2);
  width: 100%;
  text-align: center;
  color: #fff;
}

.description {
  font-size: 16px;
  margin-bottom: 20px;
  color: #ddd;
}

.select-group {
  text-align: start;
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #fff;
}

.custom-dropdown {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #fff;
}

@media (max-width:817px) {
  .container {
    width: 75%;
  }
}

@media (max-width:600px) {
  .container {
    width: 95%;
  }
}
</style>
