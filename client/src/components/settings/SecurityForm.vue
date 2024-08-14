<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >

    <v-text-field
      v-model="password.old"
      :append-inner-icon="showConfirm ? 'mdi-eye' : 'mdi-eye-off'"
      label="Old password"
      required
      :rules="passwordRules"
      :type="showOld ? 'text' : 'password'"
      @click:append-inner="showOld = !showOld"
    />
    <v-text-field
      v-model="password.new"
      :append-inner-icon="showConfirm ? 'mdi-eye' : 'mdi-eye-off'"
      label="New password"
      required
      :rules="[passwordRules,newPasswordRule(password.old)].flat()"
      :type="showNew ? 'text' : 'password'"
      @click:append-inner="showNew = !showNew"
    />

    <v-text-field
      v-model="password.confirm"
      :append-inner-icon="showConfirm ? 'mdi-eye' : 'mdi-eye-off'"
      label="Confirm new password"
      required
      :rules="[confirmedPasswordRule(password.new),newPasswordRule(password.old)].flat()"
      :type="showConfirm ? 'text' : 'password'"
      @click:append-inner="showConfirm = !showConfirm"
    />

    <v-btn
      block
      class="me-4"
      :disabled="!form?.isValid"
      text="Change Password"
      type="submit"

      @click="updateProfileSettings"
    />
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { confirmedPasswordRule, newPasswordRule, passwordRules } from '@/utilities/validators'
  import { Password, UserProfile } from '../../types/types'
  import { putSettings } from '@/api/userservice'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'SecurityForm',
    setup () {
      const notifier = useNotifier('bottom')

      const form = ref()

      const showOld = ref(false)
      const showNew = ref(false)
      const showConfirm = ref(false)

      const password = ref<Password>(
        {
          old: '',
          new: '',
          confirm: '',
        }
      )

      const updateProfileSettings = async () => {
        const userProfile: Partial<UserProfile> = { password: password.value.new }
        putSettings(userProfile)
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
        password,
        showOld,
        showNew,
        showConfirm,
        passwordRules,
        newPasswordRule,
        confirmedPasswordRule,
        updateProfileSettings,
      }
    },
  }
</script>
