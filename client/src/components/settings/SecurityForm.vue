<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >

    <v-text-field
      v-model="state.oldPassword"
      :append-icon="showOld ? 'mdi-eye' : 'mdi-eye-off'"
      clearable
      label="Old password"
      required
      :rules="passwordRules"
      :type="showOld ? 'text' : 'password'"
      @click:append="showOld = !showOld"
    />
    <v-text-field
      v-model="state.originalPassword"
      :append-icon="showNew ? 'mdi-eye' : 'mdi-eye-off'"
      clearable
      label="New password"
      required
      :rules="passwordRules"
      :type="showNew ? 'text' : 'password'"
      @click:append="showNew = !showNew"
    />

    <v-text-field
      v-model="state.confirmPassword"
      :append-icon="showConfirm ? 'mdi-eye' : 'mdi-eye-off'"
      label="Confirm new password"
      required
      :rules="confirmedPasswordRule(state.originalPassword)"
      :type="showConfirm ? 'text' : 'password'"
      @click:append="showNew = !showNew"
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
    oldPassword: string,
    originalPassword: string,
    confirmPassword: string,
  }

  export default {

    name: 'SecurityForm',
    setup () {
      const notifier = useNotifier('bottom')

      const form = ref()

      const showOld = ref(false)
      const showNew = ref(false)
      const showConfirm = ref(false)

      const state = ref<FormState>(
        {
          oldPassword: '',
          originalPassword: '',
          confirmPassword: '',
        }
      )

      const putProfileSettings = async () => {
        putSettings(state.value.originalPassword)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: 'Password changed Successfully',
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
          })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not change password',
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            console.error(err)
          })
      }

      return {
        form,
        state,
        showOld,
        showNew,
        showConfirm,
        passwordRules,
        confirmedPasswordRule,
        putProfileSettings,
      }
    },
  }
</script>
