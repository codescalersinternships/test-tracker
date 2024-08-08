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
  import { putSettings } from '@/api/userservice'
  import { useNotifier } from 'vue3-notifier'

  type FormState = {
    originalPassword: string,
    confirmPassword: string,
  }

  export default {

    name: 'SecurityForm',
    setup () {
      const notifier = useNotifier()

      const form = ref()

      const state = ref<FormState>(
        {
          originalPassword: '',
          confirmPassword: '',
        }
      )

      const putProfileSettings = async () => {
        putSettings(state.value.originalPassword)
          .then((response: any) => {
            notifier.notify()
          })
          .catch((err: any) => {
            notifier.notify()
            console.error(err)
          })
      }

      return {
        form,
        state,
        passwordRules,
        confirmedPasswordRule,
        putProfileSettings,
      }
    },
  }
</script>
