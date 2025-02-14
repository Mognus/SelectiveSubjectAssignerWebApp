<script setup lang="ts">
import { ref } from 'vue';
import Dropdown from 'primevue/dropdown';
import Card from 'primevue/card';
import Button from 'primevue/button';

const firstChoice = ref('');
const secondChoice = ref('');
const thirdChoice = ref('');
const options = ref<string[]>(['Option A', 'Option B', 'Option C', 'Option D']);
</script>

<template>
  <div class="home">
    <div class="container">
      <Card class="custom-card">
        <template #title>
          Wahlpflichtfach Manager
        </template>
        <template #content>
          <p class="description">
            Bitte wähle die Kurse aus, diese Sie künftig besuchen möchtest.
          </p>

          <div class="select-group">
            <label for="first">1. Wunsch</label>
            <Dropdown v-model="firstChoice" :options="options" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <div class="select-group">
            <label for="second">2. Wunsch</label>
            <Dropdown v-model="secondChoice" :options="options" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <div class="select-group">
            <label for="third">3. Wunsch</label>
            <Dropdown v-model="thirdChoice" :options="options" placeholder="Wähle eine Option" class="custom-dropdown" />
          </div>

          <br>
          <Button label="Absenden" class="confirm-button" />
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

/* Media Querries */
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
