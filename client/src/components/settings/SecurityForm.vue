<template>
  <v-form
    ref="form"
    fast-fail
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
      :rules="confirmedPasswordRule(state.originalPassword)"
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
      :disabled="!form?.isValid"
      text="Change Password"
      type="submit"

      @click="putProfileSettings"
    />
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { confirmedPasswordRule, passwordRules } from '@/utilities/validators'
  import { AlertType } from '@/types/types'
  import { putSettings } from '@/api/userservice'

  type FormState = {
    originalPassword: string,
    confirmPassword: string,
  }

  export default {

    name: 'SecurityForm',
    setup () {
      const form = ref()

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
        console.log('entered')
        alert.value = true
        putSettings(state.value.originalPassword)
          .then((response: any) => {
            alertType.value = AlertType.Success
            alertText.value = 'Password changed Successfully'
          })
          .catch((err: any) => {
            alertType.value = AlertType.error
            alertText.value = 'Can not change password'
            console.error(err)
          })
      }

      return {
        form,
        state,
        alert,
        alertType,
        alertText,
        passwordRules,
        confirmedPasswordRule,
        putProfileSettings,
      }
    },
  }
</script>
