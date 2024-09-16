// Utilities
import { defineStore } from 'pinia'

export const useCurrentRouteStore = defineStore('route', {
  state: () => {
    return { routeName: 'dashboard' }
  },
  actions: {
    changeCurrentRoute (name: string) {
      this.routeName = name
    },
  },
})
