/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { useCurrentRouteStore } from '../stores/route'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Home route
    { path: '', name: 'dashboard', component: () => import('@/pages/dashboard/DashboardView.vue') },
    // Nav bar routes
    { path: '/members', name: 'members', component: () => import('@/pages/members/MembersView.vue') },
    { path: '/projects', name: 'projects', component: () => import('@/pages/projects/ProjectsView.vue') },
    { path: '/settings', name: 'settings', component: () => import('@/pages/settings/SettingsView.vue') },
    // Nav bar routes
    { path: '/signup', name: 'signup', component: () => import('@/pages/authorization/SignupView.vue') },
    { path: '/signup-invitation', name: 'signup-invitation', component: () => import('@/pages/authorization/SignupInvitationView.vue') },
    { path: '/login', name: 'login', component: () => import('@/pages/authorization/LoginView.vue') },
    { path: '/logout', name: 'logout', component: () => import('@/pages/authorization/LogoutView.vue') },
    // project routes
    { path: `/projects/:projectId`, name: 'projectDetails', component: () => import('@/pages/projects/ProjectDetailsView.vue'), props: true },
    { path: '/projects/:projectId/test-plan', name: 'testPlans', component: () => import('@/pages/test-plans/TestPlansView.vue'), props: true },
    { path: '/projects/:projectId/requirement', name: 'testRequirements', component: () => import('@/pages/test-requirements/TestRequirementsView.vue'), props: true },
    { path: '/projects/:projectId/test-suite', name: 'testSuites', component: () => import('@/pages/test-suites/TestSuitesView.vue'), props: true },
    { path: '/projects/:projectId/test-run', name: 'testRuns', component: () => import('@/pages/test-runs/TestRunsView.vue'), props: true },
    { path: '/projects/:projectId/test-plan/:testPlanId', name: 'testPlan', component: () => import('@/pages/test-plans/TestPlanDetailsView.vue'), props: true },
    { path: '/projects/:projectId/requirement/:testRequirementId', name: 'testRequirement', component: () => import('@/pages/test-requirements/TestRequirementDetailsView.vue'), props: true },
    { path: '/projects/:projectId/test-suite/:testSuiteId', name: 'testSuite', component: () => import('@/pages/test-suites/TestSuiteDetailsView.vue'), props: true },
    { path: '/projects/:projectId/test-run/:testRunId', name: 'testRun', component: () => import('@/pages/test-runs/TestRunDetailsView.vue'), props: true },
  ],
})

router.beforeEach((to, from, next) => {
  const routeStore = useCurrentRouteStore()
  const authRoutes = ['signup', 'signup-invitation', 'login']
  const routeName = to.name
  console.log('to', routeName)

  if (!localStorage.getItem('TEST_TRACKER_ACCESS_TOKEN') && !authRoutes.includes(routeName)) {
    routeStore.changeCurrentRoute('login')
    next({ name: 'login' })
  } else {
    routeStore.changeCurrentRoute(routeName)
    next()
  }
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
