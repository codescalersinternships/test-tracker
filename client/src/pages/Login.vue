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
                variant="outlined"
              />
              <v-text-field
                v-model="userInfo.password"
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                placeholder="Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="passwordRules"
                :type="visible ? 'password' : 'text'"
                variant="outlined"
                @click:append-inner="visible = !visible"
              />
              <v-row>
                <v-col class="d-flex justify-end">
                  <a
                    class="text-caption text-decoration-none text-grey-darken-2"
                    href="#"
                    rel="noopener noreferrer"
                    target="_blank"
                  >
                    Forgot Password?
                  </a>
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
            @click="SumbitLogIn"
          >
            Log In
          </v-btn>

          <v-divider />
          <br>

          <!-- <v-row>
          <v-col cols="6" class="d-flex justify-center">
            <LoginGithub/>
          </v-col>
          <v-col cols="6" class="d-flex justify-center">
            <LoginTFT/>
          </v-col>
        </v-row> -->

          <br>
          <v-divider />
          <br>

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

<script>
  // import LoginGithub from '@/components/LoginGithub.vue'
  import axios from '../api/axios.ts'
  import { useRouter } from 'vue-router'
  // import LoginTFT from '@/components/LoginTFT.vue'
  import { useNotifier } from 'vue3-notifier'
  import { emailRules, passwordRules } from '@/utilities/validators'

  export default {
    components: {
      // LoginGithub,
      // LoginTFT,
    },
    setup () {
      const router = useRouter()

      const notifier = useNotifier('top right')

      const userInfo = ref({
        email: '',
        password: '',
      })

      const visible = ref(true)

      async function SumbitLogIn () {
        try {
          await axios.LogInUser(userInfo.value)
          console.log(localStorage.getItem('token'))
          if (localStorage.getItem('token') != null) {
            router.push(`/profile`)
          }
        } catch (error) {
          notifier.notify({
            title: 'Fail',
            description: 'Login failed',
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
          console.error(error)
        }
      }
      const form = ref(null)

      const isFormValid = computed(() => form.value ? form.value.isValid : false)

      function CreateAccount () {
        router.push(`/signup`)
      }

      return {
        SumbitLogIn,
        CreateAccount,
        userInfo,
        visible,
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
