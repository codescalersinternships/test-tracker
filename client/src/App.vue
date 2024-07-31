<script lang="ts">
  import { RouterView } from 'vue-router'
  import NavigationBar from './layouts/NavigationBar.vue'

  export default {

    name: 'App',
    components: {
      RouterView,
      NavigationBar,
    },
    setup () {

    },
  }

</script>

<template>
  <v-app>
    <v-main>
      <NavigationBar />
      <RouterView />
    </v-main>
  </v-app>
</template>
