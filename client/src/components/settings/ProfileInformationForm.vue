<template>
  <v-form
    fast-fail
    validate-on="submit"
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

    <v-alert
      v-if="alert"
      :title="alertText"
      :type="alertType"
    />

    <v-btn
      block
      class="me-4"
      text="Submit"
      type="submit"
      @click="putProfileSettings"
    />
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { putSettings } from '@/api/axios'
  import { AlertType, ProfileSettings } from '../../types/types'
  import { nameRules, phoneNumberRules } from '@/utilities/validators'

  export default {

    name: 'ProfileInformationForm',
    setup () {
      const state = ref<ProfileSettings>(
        {
          firstName: '',
          lastName: '',
          phoneNumber: '',
        }
      )

      const email = ref<string>('test@test.com')

      const alert = ref<boolean>(false)
      const alertType = ref<AlertType>()
      const alertText = ref<string>('')

      const putProfileSettings = async () => {
        alert.value = true
        putSettings(state.value)
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
        email,
        alert,
        alertType,
        alertText,
        nameRules,
        phoneNumberRules,
        putProfileSettings,
      }
    },
  }
</script>
