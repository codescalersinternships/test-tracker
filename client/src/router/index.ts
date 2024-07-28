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
    { path: '', name: 'dashboard', component: () => import('@/pages/DashboardView.vue') },
    // Nav bar routes
    { path: '/members', name: 'members', component: () => import('@/pages/MembersView.vue') },
    { path: '/projects', name: 'projects', component: () => import('@/pages/ProjectsView.vue') },
    { path: '/settings', name: 'settings', component: () => import('@/pages/SettingsView.vue') },
    // Nav bar routes
    { path: '/signup', name: 'signup', component: () => import('@/pages/MembersView.vue') },
    { path: '/login', name: 'login', component: () => import('@/pages/ProjectsView.vue') },
    { path: '/logout', name: 'logout', component: () => import('@/pages/SettingsView.vue') },
    // new routes
    { path: '/newProject', name: 'newProject', component: () => import('@/pages/MembersView.vue') },
    { path: '/newTestPlan', name: 'newTestPlan', component: () => import('@/pages/ProjectsView.vue') },
    { path: '/newRequirment', name: 'newRequirment', component: () => import('@/pages/SettingsView.vue') },
    { path: '/newTestSuite', name: 'newTestSuite', component: () => import('@/pages/MembersView.vue') },
    { path: '/newTestRun', name: 'newTestRun', component: () => import('@/pages/ProjectsView.vue') },
    // project routes
    { path: '/projects/:id', name: 'projectDetails', component: () => import('@/pages/ProjectDetailsView.vue') },
    { path: '/projects/:id/test-plan', name: 'testPlan', component: () => import('@/pages/ProjectsView.vue') },
    { path: '/projects/:id/requirment', name: 'testRequirment', component: () => import('@/pages/SettingsView.vue') },
    { path: '/projects/:id/test-suite', name: 'testSuite', component: () => import('@/pages/MembersView.vue') },
    { path: '/projects/:id/test-run', name: 'testRun', component: () => import('@/pages/ProjectsView.vue') },
    // members routes
    { path: '/newMember', name: 'newMember', component: () => import('@/pages/MembersView.vue') },
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
