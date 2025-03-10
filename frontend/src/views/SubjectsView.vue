<script setup lang="ts">
import { ref, defineProps, onMounted } from 'vue';
import Card from 'primevue/card';
import Badge from 'primevue/badge';
import axios from '../utils/api';
import { useAuthStore } from '../stores/authStore';

const authStore = useAuthStore();
const subjects = ref<{ label: string; description: string; teacher: string; importantNote?: string }[]>([]);

const fetchSubjects = async () => {
  try {
    const response = await axios.get('/subjects/', {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    });
    subjects.value = response.data.map((subject: any) => ({
      label: subject.subject_name,
      description: subject.subject_description,
      teacher: subject.teacher || 'Unbekannter Lehrer',
      importantNote: subject.important_note || ''
    }));
  } catch (error) {
    console.error('Fehler beim Laden der Fächer', error);
  }
};

onMounted(fetchSubjects);

const props = defineProps<{ subjects?: { label: string; description: string; teacher: string; importantNote?: string }[] }>();
</script>

<template>
  <div class="subject-details">
    <div class="subject-boxes">
      <Card v-for="subject in props.subjects ?? subjects" :key="subject.label" class="subject-card">
        <template #title>
          {{ subject.label }}
        </template>
        <template #content>
          <p>{{ subject.description }}</p>
          <div class="info-row">
            <Badge class="teacher-badge">{{ subject.teacher }}</Badge>
            <Badge v-if="subject.importantNote" class="important-badge">{{ subject.importantNote }}</Badge>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.subject-details {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.subject-boxes {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
  align-items: center;
}

.subject-card {
  width: 75%;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 12px;
  text-align: start;
  color: #fff;
}

.info-row {
  gap: 1rem;
  display: flex;
  margin-top: 10px;
}

.teacher-badge {
  background: #3498db;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.important-badge {
  background: #ffcc00;
  color: #2a2727;
  padding: 5px 10px;
  border-radius: 5px;
  font-weight: bold;
}

@media (max-width:817px) {
  .subject-card {
    width: 85%;
  }
}

@media (max-width:600px) {
  .subject-card {
    width: 95%;
  }
  .info-row {
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }
}
</style>
