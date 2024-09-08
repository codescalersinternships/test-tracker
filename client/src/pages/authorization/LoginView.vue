<template>
  <div class="background pa-0">
    <v-container>
      <v-card
        class="ma-auto pa-12 pb-8"
        elevation="8"
        max-width="448"
        rounded="lg"
      >
        <v-form ref="form">
          <v-row class="d-flex justify-center" no-gutters>
            <v-col class="d-flex justify-center" style="max-width: 100px; width: 100px;">
              <v-img
                contain
                src="@/assets/logo.png"
                style="width: 100%; height: auto;"
              />
            </v-col>
          </v-row>

          <v-row class="d-flex justify-center" no-gutters>
            <v-col class="d-flex justify-center" style="max-width: 80px; width: 80px;">
              <p class="mt-2 text-h5 text-grey-darken-2" variant="h5">Welcome</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <p class="text-center grey-darken-3">
                Sign in with your <strong>Test Tracker</strong> account
              </p>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="userInfo.email"
                density="compact"
                placeholder="Email"
                prepend-inner-icon="mdi-email-outline"
                :rules="emailRules"
                type="email"
                variant="outlined"
              />
              <v-text-field
                v-model="userInfo.password"
                :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                placeholder="Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="passwordRules"
                :type="passwordVisible ? 'password' : 'text'"
                variant="outlined"
                @click:append-inner="passwordVisible = !passwordVisible"
              />
              <v-row>
                <v-col class="d-flex justify-end">
                  <!-- <router-link
                    class="text-caption text-decoration-none text-grey-darken-2"
                    to="/forgot-password"
                  >
                    Forgot Password?
                  </router-link> -->
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <v-btn
            block
            class="mb-8"
            color="primary"
            :disabled="!isFormValid"
            size="large"
            variant="outlined"
            @click="SubmitLogIn"
          >
            Log In
          </v-btn>

          <!-- <v-divider class="my-4" /> -->

          <v-row>
            <v-col class="d-flex justify-center" cols="6">
              <!-- <LoginGithub /> -->
            </v-col>
            <v-col class="d-flex justify-center" cols="6">
              <!-- <TFLogin /> -->
            </v-col>
          </v-row>

          <!-- <v-divider class="my-4" /> -->

          <v-row>
            <v-col class="d-flex justify-center">
              <a class="text-caption text-decoration-none text-grey-darken-2">New to Test Tracker?</a>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn class="mb-8 w-100" color="primary" size="large" @click="CreateAccount">
                Create Account
              </v-btn>
            </v-col>
          </v-row>

        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script lang="ts">
  import api from '@/api/authService'
  import { useRouter } from 'vue-router'
  import { useNotifier } from 'vue3-notifier'
  import { emailRules, passwordRules } from '@/utilities/validators'
  import type { logInInfo } from '@/types/types.ts'

  export default {
    name: 'LoginView',
    setup () {
      const router = useRouter()

      const notifier = useNotifier('top right')

      const userInfo = ref<logInInfo>({
        email: '',
        password: '',
      })

      const passwordVisible = ref(true)

      async function SubmitLogIn () {
        try {
          localStorage.removeItem('TEST_TRACKER_REFRESH_TOKEN')
          await api.logInUser(userInfo.value)
          if (localStorage.getItem('TEST_TRACKER_REFRESH_TOKEN') != null) {
            router.push(`/`)
          }
        } catch (error:any) {
          console.log('here', error)
          const errorDetail = error.response?.data?.detail
          notifier.notify({
            title: 'Fail',
            description: errorDetail,
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
        }
      }

      const form = ref(null)

      const isFormValid = computed(() => form.value ? (form.value as any).isValid : false)

      function CreateAccount () {
        router.push(`/signup`)
      }

      return {
        SubmitLogIn,
        CreateAccount,
        userInfo,
        passwordVisible,
        notifier,
        isFormValid,
        emailRules,
        passwordRules,
        form,
      }
    },
  }
</script>

<style>
.background {
background-image: url('@/assets/authPagesBackGround.png');
background-size: cover;
background-position: center;
background-repeat: no-repeat;
padding: 0px;
margin: 0px;
width: 100%;
height: 100%;
}
</style>
