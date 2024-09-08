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

          <v-row class="d-flex justify-center mb-4" no-gutters>
            <v-col class="d-flex justify-center" style="max-width: 80px; width: 80px;">
              <p class="mt-2 text-h5 text-grey-darken-2 font-weight-bold" variant="h5">Hello {{ firstName }}</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <p class="font-weight-bold text-grey-darken-3">@{{ invitor }}</p>
              <p class="text-grey-darken-3"> has invited you to join the </p>
              <p class="font-weight-bold text-grey-darken-3">Test Tracker App</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <p class="text-center text-grey-darken-3">
                Write your password to confirm the registration
              </p>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="userPassword.password"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                placeholder="Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="passwordRules"
                :type="showPassword ? 'password' : 'text'"
                variant="outlined"
                @click:append-inner="showPassword = !showPassword"
              />
              <v-text-field
                v-model="userPassword.password2"
                :append-inner-icon="showRePassword ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                placeholder="Re Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="confirmedPasswordRules"
                :type="showRePassword ? 'password' : 'text'"
                variant="outlined"
                @click:append-inner="showRePassword = !showRePassword"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn
                class="mb-8 w-100"
                color="primary"
                :disabled="!isFormValid"
                size="large"
                @click="RegisterUser"
              >
                Register
              </v-btn>
            </v-col>
          </v-row>

          <v-divider class="my-4" />
          <LoginHintComponent />
        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script>
  import api from '@/api/authService'
  import { useRouter } from 'vue-router'
  import { useNotifier } from 'vue3-notifier'
  import { confirmedPasswordRule, passwordRules } from '@/utilities/validators'
  import LoginHintComponent from '@/components/LoginHintComponent.vue'

  export default {
    name: 'SignupInvitationView',
    components: {
      LoginHintComponent,
    },
    setup () {
      const router = useRouter()
      const notifier = useNotifier('top right')

      const userPassword = ref({
        password: '',
        password2: '',
      })

      const showPassword = ref(true)
      const showRePassword = ref(true)

      const firstName = ref('')
      const invitor = ref('')

      async function RegisterUser () {
        try {
          await api.signUpInvitation(userPassword.value.password)
          notifier.notify({
            title: 'Success',
            description: 'successful sign up',
            showProgressBar: true,
            timeout: 7_000,
            type: 'success',
          })
        } catch (error) {
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

      function LogIn () {
        router.push(`/`)
      }

      const isFormValid = computed(() => form.value ? form.value.isValid : false)
      const confirmedPasswordRules = computed(() => confirmedPasswordRule(userPassword.value.password))

      const form = ref(null)

      return {
        userPassword,
        showPassword,
        showRePassword,
        RegisterUser,
        LogIn,
        firstName,
        invitor,
        passwordRules,
        confirmedPasswordRule,
        form,
        isFormValid,
        confirmedPasswordRules,
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
