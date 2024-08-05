<template>
  <v-form
    fast-fail
    validate-on="submit"
    @submit.prevent
  >
    <v-text-field
      v-model="state.originalPassword"
      label="Password"
      required
      :rules="passwordRules"
      type="password"
    />

    <v-text-field
      v-model="state.confirmPassword"
      label="Confirm Password"
      required
      :rules="passwordRules"
      type="password"
    />

    <v-alert
      v-if="alert"
      :title="alertText"
      :type="alertType"
    />

    <v-btn
      block
      class="me-4"
      text="Change Password"
      type="submit"
      @click="putProfileSettings"
    />
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { passwordRules } from '@/utilities/validators'
  import { AlertType } from '@/types/types'
  import { putSettings } from '@/api/axios'

  type FormState = {
    originalPassword: string,
    confirmPassword: string,
  }

  export default {

    name: 'SecurityForm',
    setup () {
      const state = ref<FormState>(
        {
          originalPassword: '',
          confirmPassword: '',
        }
      )

      const alert = ref<boolean>(false)
      const alertType = ref<AlertType>()
      const alertText = ref<string>('')

      const putProfileSettings = async () => {
        alert.value = true
        putSettings(state.value.originalPassword)
          .catch(response => {
            const { err } = response.response.data
            if (err != null) {
              alertType.value = AlertType.error
              alertText.value = 'Can not change password'
              return
            }
            alertType.value = AlertType.Success
            alertText.value = 'Password changed Successfully'
          })
      }

      return {
        state,
        alert,
        alertType,
        alertText,
        passwordRules,
        putProfileSettings,
      }
    },
  }
</script>
