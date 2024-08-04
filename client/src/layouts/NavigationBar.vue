<template>
  <v-app-bar
    class="px-9"
    color="teal-darken-4"
  >
    <div class="app-component mx-9">
      <RouterLink
        v-for="(item,index) in mainRoutes"
        :key="index"
        class="mx-3 text-white bg-teal-darken-3 pa-3 rounded-lg font-weight-black"
        :to="{ name: item.routeName}"
      >
        {{ item.displayName }}
      </RouterLink>
    </div>

    <div class="app-component mx-9">
      <v-menu transition="fab-transition">
        <template #activator="{ props }">
          <v-btn v-if="displayMenuRoutes(routeStore.routeName)" icon="mdi-plus" size="large" v-bind="props" />
        </template>
        <v-list>
          <v-list-item
            v-for="(item,index) in menuRoutes"
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
    </div>

  </v-app-bar>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { RouterLink } from 'vue-router'
  import { useCurrentRouteStore } from '../stores/route'

  type AppRoute = {
    displayName: string,
    routeName: string,
  }

  export default {

    name: 'NavigationBar',
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
        displayMenuRoutes,
        RouterLink,
      }
    },
    computed: {
      mainRoutes () {
        const routeName = this.routeStore.routeName

        if (routeName === 'dashboard' || routeName === 'settings') {
          return [
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
            {
              displayName: 'Settings',
              routeName: 'settings',
            },
          ]
        } else if (routeName === 'projectDetails') {
          return [
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
            {
              displayName: 'Test Plan',
              routeName: 'testPlan',
            },
            {
              displayName: 'Requirement',
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
          ]
        }
        return [
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
      },
      menuRoutes () {
        const routeName = this.routeStore.routeName

        if (routeName === 'projects') {
          return [
            {
              displayName: 'New Project',
              routeName: 'newProject',
            },
          ]
        }

        if (routeName === 'projectDetails') {
          return [
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
        }

        if (routeName === 'testPlan') {
          return [
            {
              displayName: 'New Test Plan',
              routeName: 'newTestPlan',
            },
          ]
        }

        if (routeName === 'testRequirment') {
          return [
            {
              displayName: 'New Requirment',
              routeName: 'newRequirment',
            },
          ]
        }

        if (routeName === 'testSuite') {
          return [
            {
              displayName: 'New Test Suite',
              routeName: 'newTestSuite',
            },
          ]
        }

        if (routeName === 'testRun') {
          return [
            {
              displayName: 'New Test Run',
              routeName: 'newTestRun',
            },
          ]
        }

        if (routeName === 'members') {
          return [
            {
              displayName: 'Invite Member',
              routeName: 'newMember',
            },
          ]
        }

        return []
      },
    },
  }
</script>

<style lang="scss" scoped>

a {
  text-decoration: none;
  color: inherit;
  font-size: 0.75rem;
}

::v-deep .v-toolbar__content {
  display: flex !important;
  justify-content: space-between !important;
}

</style>
