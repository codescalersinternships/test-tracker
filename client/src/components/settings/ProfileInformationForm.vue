<template>
  <v-form>
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
      class="me-4"
      type="submit"
      @click.stop.prevent="putProfileSettings"
    >
      submit
    </v-btn>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { putSettings } from '@/api/axios'
  import { ProfileSettings } from '../../types/types'
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

      const done = ref<boolean>(false)

      const putProfileSettings = async () => {
        putSettings(state.value)
          .catch(response => {
            const { err } = response.response.data
            if (err != null) {
              done.value = false
            }
            done.value = true
          })
      }

      return {
        state,
        email,
        nameRules,
        phoneNumberRules,
        putProfileSettings,
      }
    },
  }
</script>
