<template>
  <v-app>
    <v-main>
      <div class="background pa-0">
        <NavigationBar v-if="displayNavBar(routeStore.routeName)" />
        <RouterView />
      </div>
    </v-main>
  </v-app>
</template>

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

<style lang="scss">
  .background {
    background-image: url('/testtrackerbackground.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    padding: 0px;
    margin: 0px;
    width: 100%;
    height: 100%;
  }
</style>
