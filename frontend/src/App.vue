<script setup lang="ts">
import NavBarComponent from "./components/NavBarComponent.vue";
</script>

<template>
  <div class="app-container">
    <NavBarComponent />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  backdrop-filter: blur(10px);
}

main {
  height: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #fff;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}
</style>
