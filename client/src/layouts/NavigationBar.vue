<template>
  <v-app-bar
    color="teal-darken-4"
  >
    <v-spacer />
    <RouterLink
      v-for="(item,index) in navigationRoutes"
      :key="index"
      class="mx-3 text-white bg-teal-darken-3 pa-3 rounded-xl font-weight-black"
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
        <v-btn icon="mdi-plus" size="large" v-bind="props" />
      </template>
      <v-list>
        <v-list-item
          v-for="(item,index) in [...defaultRoutes,...additionalRoutes]"
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
  import { defineComponent, type PropType, ref } from 'vue'
  import { RouterLink } from 'vue-router'

  type AppRoute = {
    displayName: string,
    routeName: string,
  }

  export default defineComponent({
    props: {
      menuRoutes: {
        required: false,
        type: Array as PropType<AppRoute[]>,
      },
    },
    setup (props) {
      const navigationRoutes = [
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
      const profileRoutes = [
        {
          displayName: 'Settings',
          routeName: 'settings',
        },
        {
          displayName: 'Logout',
          routeName: 'logout',
        },
      ]

      const defaultRoutes = ref<AppRoute[]>(
        [{
          displayName: 'New Project',
          routeName: 'newProject',
        }]
      )
      const additionalRoutes = ref<AppRoute[]>(
        props.menuRoutes || [] as AppRoute[]
      )
      return {
        defaultRoutes,
        additionalRoutes,
        navigationRoutes,
        profileRoutes,
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
