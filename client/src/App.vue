<script lang="ts" setup>
  import { RouterView } from 'vue-router'
  import NavigationBar from './layouts/NavigationBar.vue'

  const routes = [

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
</script>

<template>
  <v-app>
    <v-main>
      <NavigationBar />
      <RouterView />
    </v-main>
  </v-app>
</template>
