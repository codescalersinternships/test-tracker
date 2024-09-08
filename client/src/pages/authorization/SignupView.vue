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
              <p class="mt-2 text-h5 text-grey-darken-2" variant="h5">Sign up</p>
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model="newUser.first_name"
                density="compact"
                placeholder="First Name"
                prepend-inner-icon="mdi-account-outline"
                :rules="nameRules"
                variant="outlined"
              />
              <v-text-field
                v-model="newUser.last_name"
                density="compact"
                placeholder="Last Name"
                prepend-inner-icon="mdi-account-outline"
                :rules="nameRules"
                variant="outlined"
              />
              <v-text-field
                v-model="newUser.email"
                density="compact"
                placeholder="Email"
                prepend-inner-icon="mdi-email-outline"
                :rules="emailRules"
                type="email"
                variant="outlined"
              />
              <v-text-field
                v-model="newUser.password"
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                placeholder="Password"
                prepend-inner-icon="mdi-lock-outline"
                :rules="passwordRules"
                :type="visible ? 'password' : 'text'"
                variant="outlined"
                @click:append-inner="visible = !visible"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex justify-center">
              <v-btn
                block
                class="mb-8 w-100"
                color="primary"
                :disabled="!isFormValid"
                :loading="loading"
                size="large"
                @click="RegisterNewUser"
              >
                Register
              </v-btn>
            </v-col>
          </v-row>

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
          <LoginHintComponent />
        </v-form>

      </v-card>
    </v-container>
  </div>
</template>

<script lang="ts">
  import api from '@/api/authService'
  import { useNotifier } from 'vue3-notifier'
  import { useRouter } from 'vue-router'
  import { emailRules, nameRules, passwordRules } from '@/utilities/validators'
  import LoginHintComponent from '@/components/LoginHintComponent.vue'
  import { signUpInfo } from '@/types/types'

  export default {
    name: 'SignupView',
    components: {
      LoginHintComponent,
    },
    setup () {
      const notifier = useNotifier('top right')
      const router = useRouter()
      const loading = ref(false)

      const newUser = ref<signUpInfo>({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
      })

      const visible = ref(true)

      async function RegisterNewUser () {
        loading.value = true
        try {
          await api.signUp(newUser.value)
          loading.value = false
          notifier.notify({
            title: 'Success',
            description: 'successful sign up',
            showProgressBar: true,
            timeout: 7_000,
            type: 'success',
          })
          router.push(`/login`)
        } catch (error:any) {
          const errorDetail = error.response?.data?.detail
          notifier.notify({
            title: 'Fail',
            description: errorDetail,
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
          console.error(error)
        } finally {
          loading.value = false
        }
      }
      const form = ref(null)
      const isFormValid = computed(() => form.value ? (form.value as any).isValid : false)

      return {
        RegisterNewUser,
        visible,
        newUser,
        notifier,
        loading,
        form,
        emailRules,
        passwordRules,
        nameRules,
        isFormValid,
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
