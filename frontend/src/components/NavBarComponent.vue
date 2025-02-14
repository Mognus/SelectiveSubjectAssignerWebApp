<script setup lang="ts">
import Button from 'primevue/button';
</script>

<template>
  <div class="navbar-wrapper">
    <div class="nav-bar">
      <div class="nav-logo">
        <img class="logo" src="../assets/vue.svg" alt="" />
      </div>
      <div class="nav-items">
        <router-link to="/" active-class="active" class="button">Auswahl</router-link>
        <router-link to="/subjects" active-class="active" class="button">Fächer</router-link>
      </div>
      <div class="actions">
        <Button label="Login" />
      </div>
    </div>
  </div>
</template>

<style scoped>
a {
  text-decoration: none;
  color: white;
}

a:hover{
  color: rgb(195, 238, 221);
}

a:active{
  color: rgb(160, 211, 191);
}

.active{
  color: rgb(110, 231, 183);
}

.navbar-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-bar{
  padding: 0.5rem 1rem;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 35%;
  background: rgba(255, 255, 255, 0.32);
}

.nav-items {
  color: white;
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

a.active:before, a:hover:before {
  background: snow;
  opacity: .8;
}

a:before {
  background: #0a0505;
  border-radius: 10px;
  bottom: 0;
  content: "";
  height: 3px;
  left: 0;
  opacity: .2;
  position: absolute;
  width: 100%;
}

/* Media Querries */
@media (max-width:817px) {
 .nav-bar {
    width: 75%;
  }
}

@media (max-width:380px) {
 .nav-bar {
    width: 95%;
  }
}
</style>