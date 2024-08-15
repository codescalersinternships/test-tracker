<script lang="ts">
  import { RouterView } from 'vue-router'
  import NavigationBar from '@/layouts/NavigationBar.vue'
  import { useCurrentRouteStore } from './stores/route'

  export default {

    name: 'App',
    components: {
      RouterView,
      NavigationBar,
    },
    setup () {
      const routeStore = useCurrentRouteStore()

      function displayNavBar (routeName: string): boolean {
        const authRoutes = ['signup', 'signup-invitation', 'login', 'logout']
        return !authRoutes.includes(routeName)
      }

      return {
        routeStore,
        displayNavBar,
      }
    },
  }

</script>

<template>
  <v-app>
    <v-main>
      <NavigationBar v-if="displayNavBar(routeStore.routeName)" />
      <RouterView />
    </v-main>
  </v-app>
</template>
