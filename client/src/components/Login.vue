<template>
  <v-row>
    <v-col class="d-flex justify-center">
      <p class="text-caption text-decoration-none text-grey-darken-2">
        Already have an account?
        <router-link
          class="text-caption text-decoration-none text-blue"
          to="/login"
        >
          Sign in
        </router-link>
      </p>
    </v-col>
  </v-row>
</template>

<script>
  import { useRouter } from 'vue-router'

  export default {
    setup () {
      const router = useRouter()
      function handleLogIn () {
        router.push(`/login`)
      }
      return {
        handleLogIn,
      }
    },
  }
</script>
