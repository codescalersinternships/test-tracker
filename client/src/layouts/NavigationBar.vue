<template>
  <v-app-bar
    color="teal-darken-4"
  >
    <v-spacer />
    <RouterLink
      v-for="(item,index) in createMainRoutes(routeStore.routeName)"
      :key="index"
      class="mx-3 text-white bg-teal-darken-3 pa-3 rounded-lg font-weight-black"
      :to="{ name: item.routeName}"
    >
      {{ item.displayName }}
    </RouterLink>

    <v-spacer />
    <v-spacer />
    <v-spacer />
    <v-spacer />
    <v-spacer />

    <v-menu transition="fab-transition">
      <template #activator="{ props }">
        <v-btn v-if="displayMenuRoutes(routeStore.routeName)" icon="mdi-plus" size="large" v-bind="props" />
      </template>
      <v-list>
        <v-list-item
          v-for="(item,index) in createMenuRoutes(routeStore.routeName)"
          :key="index"
        >
          <RouterLink class="mx-3 text-white pa-3 font-weight-black" :to="{ name: item.routeName}">
            {{ item.displayName }}
          </RouterLink>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-menu transition="fab-transition">
      <template #activator="{ props }">
        <v-btn icon="mdi-account" size="large" v-bind="props" />
      </template>
      <v-list>
        <v-list-item
          v-for="(item,index) in profileRoutes"
          :key="index"
        >
          <RouterLink class="mx-3 text-white pa-3 font-weight-black" :to="{ name: item.routeName}">
            {{ item.displayName }}
          </RouterLink>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-spacer />
  </v-app-bar>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue'
  import { RouterLink } from 'vue-router'
  import { useCurrentRouteStore } from '../stores/route'

  type AppRoute = {
    displayName: string,
    routeName: string,
  }

  export default defineComponent({

    setup () {
      const routeStore = useCurrentRouteStore()

      const profileRoutes = ref<AppRoute[]>(
        [
          {
            displayName: 'Settings',
            routeName: 'settings',
          },
          {
            displayName: 'Logout',
            routeName: 'logout',
          },
        ]
      )

      function createMainRoutes (routeName: string): AppRoute[] {
        const mainRoutes: AppRoute[] =
          [
            {
              displayName: 'Dashboard',
              routeName: 'dashboard',
            },
            {
              displayName: 'Members',
              routeName: 'members',
            },
            {
              displayName: 'Projects',
              routeName: 'projects',
            },
          ]

        if (routeName === 'dashboard') {
          mainRoutes.push(
            {
              displayName: 'Settings',
              routeName: 'settings',
            },
          )
        } else if (routeName === 'projectDetails') {
          mainRoutes.push(
            {
              displayName: 'Test Plan',
              routeName: 'testPlan',
            },
            {
              displayName: 'Requirment',
              routeName: 'testRequirment',
            },
            {
              displayName: 'Test Suite',
              routeName: 'testSuite',
            },
            {
              displayName: 'Test Run',
              routeName: 'testRun',
            },
          )
        }
        return mainRoutes
      }

      function createMenuRoutes (routeName: string): AppRoute[] {
        const menuRoutes: AppRoute[] = []

        if (routeName === 'projects') {
          menuRoutes.push(
            {
              displayName: 'New Project',
              routeName: 'newProject',
            }
          )
        }

        if (routeName === 'projectDetails') {
          menuRoutes.push(
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
          )
        }

        if (routeName === 'testPlan') {
          menuRoutes.push(
            {
              displayName: 'New Test Plan',
              routeName: 'newTestPlan',
            },
          )
        }

        if (routeName === 'testRequirment') {
          menuRoutes.push(
            {
              displayName: 'New Requirment',
              routeName: 'newRequirment',
            },
          )
        }

        if (routeName === 'testSuite') {
          menuRoutes.push(
            {
              displayName: 'New Test Suite',
              routeName: 'newTestSuite',
            },
          )
        }

        if (routeName === 'testRun') {
          menuRoutes.push(
            {
              displayName: 'New Test Run',
              routeName: 'newTestRun',
            },
          )
        }

        if (routeName === 'members') {
          menuRoutes.push(
            {
              displayName: 'Invite Member',
              routeName: 'newMember',
            },
          )
        }

        return menuRoutes
      }

      function displayMenuRoutes (routeName: string): boolean {
        if (routeName === 'dashboard') {
          return false
        }

        if (routeName === 'settings') {
          return false
        }

        return true
      }

      return {
        profileRoutes,
        routeStore,
        createMenuRoutes,
        createMainRoutes,
        displayMenuRoutes,
        RouterLink,
      }
    },
  })
</script>

<style lang="scss" scoped>

a {
  text-decoration: none;
  color: inherit;
  font-size: 0.75rem;
}

</style>
