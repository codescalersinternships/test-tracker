<template>
  <v-app-bar
    class="px-9"
    color="white"
    height="75"
  >
    <div class="app-component mx-9 d-flex">
      <div class="left-nav-bar">
        <RouterLink
          :to="{ name: 'dashboard' }"
        >
          <v-img
            alt="Test Tracker Logo"
            contain
            src="/testtrackerlogo.png"
            style="width: 188.5px; height: 50px;"
          />
        </RouterLink>
      </div>

      <div class="right-nav-bar">
        <RouterLink
          v-for="(item,index) in mainRoutes"
          :key="index"
          class="mx-5 text-blue bg-white pa-3 rounded-lg font-weight-black"
          :to="{ name: item.routeName }"
        >
          {{ item.displayName }}
        </RouterLink>
      </div>

    </div>

    <div class="app-component mx-9">
      <v-menu transition="fab-transition">
        <template #activator="{ props }">
          <v-btn
            v-if="displayForms(routeStore.routeName)"
            class="mx-3 bg-blue"
            color="white"
            icon="mdi-plus"
            size="large"
            v-bind="props"
          />
        </template>
        <v-list>
          <v-list-item
            v-for="(item,index) in newForms"
            :key="index"
          >
            <v-btn>
              {{ item.displayName }}

              <v-overlay
                activator="parent"
                location="left"
                scroll-strategy="reposition"
              >
                <component :is="item.component" />
              </v-overlay>
            </v-btn>
          </v-list-item>
          <!-- to be integrated with new forms -->
        </v-list>
      </v-menu>

      <v-menu transition="fab-transition">
        <template #activator="{ props }">
          <v-btn
            class="bg-blue"
            color="white"
            icon="mdi-account"
            size="large"
            v-bind="props"
          />
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
  import ProjectForm from '@/components/projects/ProjectForm.vue'
  import TestPlanForm from '@/components/test-plans/TestPlanForm.vue'
  import TestRequirementForm from '@/components/test-requirements/TestRequirementForm.vue'
  import TestSuiteForm from '@/components/test-suites/TestSuiteForm.vue'
  import TestRunForm from '@/components/test-runs/TestRunForm.vue'
  import MemberForm from '@/components/members/MemberForm.vue'

  type AppRoute = {
    displayName: string,
    routeName: string,
  }

  export default {
    name: 'NavigationBar',

    components: {
      ProjectForm,
      MemberForm,
      TestPlanForm,
      TestRequirementForm,
      TestRunForm,
      TestSuiteForm,
    },
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

      function displayForms (routeName: string): boolean {
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
        displayForms,
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
        const routeName = this.routeStore.routeName

        if (routeName === 'projects') {
          return [
            {
              displayName: 'New Project',
              component: ProjectForm,
            },
          ]
        } else if (routeName === 'projectDetails') {
          return [
            {
              displayName: 'New Test Plan',
              component: TestPlanForm,
            },
            {
              displayName: 'New Requirement',
              component: TestRequirementForm,
            },
            {
              displayName: 'New Test Suite',
              component: TestSuiteForm,
            },
            {
              displayName: 'New Test Run',
              component: TestRunForm,
            },
          ]
        } else if (routeName === 'testPlans') {
          return [
            {
              displayName: 'New Test Plan',
              component: TestPlanForm,
            },
          ]
        } else if (routeName === 'testRequirements') {
          return [
            {
              displayName: 'New Requirement',
              component: TestRequirementForm,
            },
          ]
        } else if (routeName === 'testSuites') {
          return [
            {
              displayName: 'New Test Suite',
              component: TestSuiteForm,
            },
          ]
        } else if (routeName === 'testRuns') {
          return [
            {
              displayName: 'New Test Run',
              component: TestRunForm,
            },
          ]
        } else {
          return []
        }
      },
    },
  }
</script>

<style lang="scss" scoped>

a {
  text-decoration: none;
  color: inherit;
  font-size: 1rem;
}

.left-nav-bar {
  width: 250px;
}
.right-nav-bar {
  width: 50%;
  padding-top: 3px;
  display: flex;
}

::v-deep .v-toolbar__content {
  display: flex !important;
  justify-content: space-between !important;
}

.v-btn--icon.v-btn--density-default {
  width: calc(var(--v-btn-height) + 3px);
  height: calc(var(--v-btn-height) + 3px);
}

</style>
