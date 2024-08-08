<template>
  <v-app-bar
    class="px-9"
    color="white"
    height="75"
  >
    <div class="app-component mx-9">
      <div class="left-nav-bar">
        <v-img
          alt="Test Tracker Logo"
          contain
          src="/navbarlogo.png"
          style="width: 188.5px; height: 30px;"
        />
      </div>

      <div class="right-nav-bar">
        <RouterLink
          v-for="(item,index) in mainRoutes"
          :key="index"
          class="mx-5 text-blue bg-white pa-3 rounded-lg font-weight-black"
          :to="{ name: item.routeName}"
        >
          {{ item.displayName }}
        </RouterLink>
      </div>

    </div>

    <div class="app-component mx-9">
      <v-menu transition="fab-transition">
        <template #activator="{ props }">
          <v-btn
            v-if="displayMenuRoutes(routeStore.routeName)"
            color="blue"
            icon="mdi-plus-circle"
            size="x-large"
            v-bind="props"
          />
        </template>
        <v-list>
          <v-list-item
            v-for="(item,index) in newForms"
            :key="index"
          />
          <v-btn class="mx-3  pa-3 font-weight-black text-blue">
            {{ item.displayName }}
          </v-btn>
        </v-list>
      </v-menu>

      <v-menu transition="fab-transition">
        <template #activator="{ props }">
          <v-btn color="blue" icon="mdi-account" size="x-large" v-bind="props" />
        </template>
        <v-list>
          <v-list-item
            v-for="(item,index) in profileRoutes"
            :key="index"
          >
            <RouterLink class="mx-3 pa-3 font-weight-black text-blue" :to="{ name: item.routeName}">
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
              routeName: 'testRequirement',
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
      newForms () {
        return []
      },
    },
  }
</script>

<style lang="scss" scoped>

a {
  text-decoration: none;
  color: inherit;
  font-size: 0.9rem;
}

.left-nav-bar {
  width: 250px;
  float: left;
}
.right-nav-bar {
  width: 50%;
  float: left;
  padding-top: 3px;
}

::v-deep .v-toolbar__content {
  display: flex !important;
  justify-content: space-between !important;
}

</style>
