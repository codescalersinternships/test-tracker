<template>
  <v-btn class="w-100" variant="outlined" @click="SubmitLoginGithub">
    <v-icon left>mdi-github</v-icon>
    Github
  </v-btn>
</template>

<script>
  import { getToken, getUser } from '@/helpers/githubLogin.ts'
  export default {
    setup () {
      async function SubmitLoginGithub () {
        try {
          const accessToken = await getToken(code)
          const user = await getUser(accessToken)
          const token = user.data.result.access_token
          localStorage.setItem('token', token)
          window.location.href = '/'
        } catch (error) {
          console.error(error)
        }
      }

      return {
        SubmitLoginGithub,
      }
    },
  }
</script>
