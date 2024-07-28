<script lang="ts" setup>
  import { RouterView } from 'vue-router'
  import NavigationBar from './layouts/NavigationBar.vue'

</script>

<template>
  <v-app>
    <v-main>
      <NavigationBar />
      <RouterView />
    </v-main>
  </v-app>
</template>
