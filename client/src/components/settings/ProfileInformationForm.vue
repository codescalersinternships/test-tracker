<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="email"
      :counter="10"
      disabled
      label="E-mail"
    />

    <v-text-field
      v-model="state.firstName"
      clearable
      label="First Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="state.lastName"
      clearable
      label="Last Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="state.phoneNumber"
      clearable
      label="Phone Number"
      :rules="phoneNumberRules"
    />

    <v-btn
      block
      class="me-4"
      :disabled="!form?.isValid"
      text="Submit"
      type="submit"

      @click="putProfileSettings"
    />
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { putSettings } from '@/api/userservice'
  import { ProfileSettings } from '../../types/types'
  import { nameRules, phoneNumberRules } from '@/utilities/validators'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProfileInformationForm',
    setup () {
      const notifier = useNotifier('bottom')

      const form = ref()

      const state = ref<ProfileSettings>(
        {
          firstName: '',
          lastName: '',
          phoneNumber: '',
        }
      )

      const email = ref<string>('test@test.com')

      const putProfileSettings = async () => {
        putSettings(state.value)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: 'Profile changed Successfully',
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
          })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not change profile',
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
        email,
        nameRules,
        phoneNumberRules,
        putProfileSettings,
      }
    },
  }
</script>
