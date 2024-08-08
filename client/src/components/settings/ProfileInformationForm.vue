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
      label="First Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="state.lastName"
      label="Last Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="state.phoneNumber"
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
      const notifier = useNotifier()

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
        alert.value = true
        putSettings(state.value)
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
        email,
        nameRules,
        phoneNumberRules,
        putProfileSettings,
      }
    },
  }
</script>
