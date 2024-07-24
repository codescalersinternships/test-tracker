<script lang="ts" setup>
  import { RouterView } from 'vue-router'
  import NavigationBar from './layouts/NavigationBar.vue'

  const menuRoutes = [

    {
      displayName: 'New Test Plan',
      routeName: 'newTestPlan',
    },
    {
      displayName: 'New Requirment',
      routeName: 'newRequirment',
    },
    {
      displayName: 'New Test Suite',
      routeName: 'newTestSuite',
    },
    {
      displayName: 'New Test Run',
      routeName: 'newTestRun',
    },
  ]

  const mainRoutes = [
    {
      displayName: 'Settings',
      routeName: 'settings',
    },
  ]
</script>

<template>
  <v-app>
    <v-main>
      <NavigationBar :main-routes="mainRoutes" :menu-routes="menuRoutes" />
      <RouterView />
    </v-main>
  </v-app>
</template>
