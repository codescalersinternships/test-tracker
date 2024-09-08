<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >

    <v-text-field
      v-model="password.old_password"
      :append-inner-icon="showOld ? 'mdi-eye' : 'mdi-eye-off'"
      base-color="blue"
      color="blue"
      label="Old password"
      required
      :rules="oldPasswordRule"
      :type="showOld ? 'text' : 'password'"
      @click:append-inner="showOld = !showOld"
    />
    <v-text-field
      v-model="password.new_password"
      :append-inner-icon="showNew ? 'mdi-eye' : 'mdi-eye-off'"
      base-color="blue"
      color="blue"
      label="New password"
      required
      :rules="[passwordRules,newPasswordRule(password.old_password)].flat()"
      :type="showNew ? 'text' : 'password'"
      @click:append-inner="showNew = !showNew"
    />

    <v-text-field
      v-model="password.confirm_password"
      :append-inner-icon="showConfirm ? 'mdi-eye' : 'mdi-eye-off'"
      base-color="blue"
      color="blue"
      label="Confirm new password"
      required
      :rules="[confirmedPasswordRule(password.new_password),newPasswordRule(password.old_password)].flat()"
      :type="showConfirm ? 'text' : 'password'"
      @click:append-inner="showConfirm = !showConfirm"
    />

    <v-col class="text-right">
      <v-btn

        class="me-4"
        color="blue"
        :disabled="!form?.isValid || loading"
        :loading="loading"
        size="large"
        text="Change Password"
        type="submit"

        @click="updatePassword"
      />
    </v-col>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { confirmedPasswordRule, newPasswordRule, oldPasswordRule, passwordRules } from '@/utilities/validators'
  import { Password } from '../../types/types'
  import { putPassword } from '@/api/userService'
  import { useNotifier } from 'vue3-notifier'
  import debounce from 'debounce'

  export default {

    name: 'SecurityForm',
    setup () {
      const notifier = useNotifier('top right')

      const form = ref()

      const showOld = ref(false)
      const showNew = ref(false)
      const showConfirm = ref(false)

      const loading = ref(false)

      const password = ref<Password>(
        {
          old_password: '',
          new_password: '',
          confirm_password: '',
        }
      )

      const updatePassword = async () => {
        loading.value = true
        const passwords: Partial<Password> = {
          old_password: password.value.old_password,
          new_password: password.value.new_password,
        }
        putPassword(passwords)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: response.data.message,
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
            loading.value = false
          })
          .catch((err: any) => {
            let description = 'Can not update password'
            if (err.response) {
              description = err.response.data.detail
            }
            notifier.notify({
              title: 'Fail',
              description,
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            loading.value = false
          })
      }

      return {
        form,
        password,
        showOld,
        showNew,
        loading,
        debounce,
        showConfirm,
        passwordRules,
        oldPasswordRule,
        newPasswordRule,
        confirmedPasswordRule,
        updatePassword,
      }
    },
  }
</script>
