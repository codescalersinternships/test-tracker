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
        if (routeName === 'signup') {
          return false
        }

        if (routeName === 'signupinvitation') {
          return false
        }

        if (routeName === 'login') {
          return false
        }

        if (routeName === 'logout') {
          return false
        }

        return true
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
