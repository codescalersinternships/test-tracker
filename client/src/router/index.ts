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
    { path: '/projects/:project-id', name: 'projectDetails', component: () => import('@/pages/projects/ProjectDetailsView.vue'), props: { 'project-id': Number } },
    { path: '/projects/:project-id/test-plan', name: 'testPlans', component: () => import('@/pages/test-plans/TestPlansView.vue'), props: { 'project-id': Number } },
    { path: '/projects/:project-id/requirement', name: 'testRequirements', component: () => import('@/pages/test-requirements/TestRequirementsView.vue'), props: { 'project-id': Number } },
    { path: '/projects/:project-id/test-suite', name: 'testSuites', component: () => import('@/pages/test-suites/TestSuitesView.vue'), props: { 'project-id': Number } },
    { path: '/projects/:project-id/test-run', name: 'testRuns', component: () => import('@/pages/test-runs/TestRunsView.vue'), props: { 'project-id': Number } },
    { path: '/projects/:project-id/test-plan/:id', name: 'testPlan', component: () => import('@/pages/test-plans/TestPlanDetailsView.vue'), props: { 'project-id': Number, 'test-plan-id': Number } },
    { path: '/projects/:project-id/requirement/:id', name: 'testRequirement', component: () => import('@/pages/test-requirements/TestRequirementDetailsView.vue'), props: { 'project-id': Number, 'test-requirement-id': Number } },
    { path: '/projects/:project-id/test-suite/:id', name: 'testSuite', component: () => import('@/pages/test-suites/TestSuiteDetailsView.vue'), props: { 'project-id': Number, 'test-suite-id': Number } },
    { path: '/projects/:project-id/test-run/:test-run-id', name: 'testRun', component: () => import('@/pages/test-runs/TestRunDetailsView.vue'), props: { 'project-id': Number, 'test-run-id': Number } },
  ],
})

router.beforeEach((to, from) => {
  const routeStore = useCurrentRouteStore()

  routeStore.changeCurrentRoute(to.name)
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
