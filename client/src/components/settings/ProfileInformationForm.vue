<template>
  <v-form>
    <v-text-field
      v-model="state.email"
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
    >
      submit
    </v-btn>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { putSettings } from '@/api/axios'
  import { ProfileSettings } from '../../types/types'

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

      const nameRules = [
        (value: string) => {
          if (value?.length > 1) return true
          return 'Name must be at least 1 character.'
        },
        (value: string) => {
          if (value?.length < 51) return true
          return 'Name must be at most 50 characters.'
        },
        (value: string) => {
          if (/[^0-9]/.test(value)) return true
          return 'Name can not contain digits.'
        },
      ]

      const phoneNumberRules = [
        (value: string) => {
          if (value?.length < 21) return true
          return 'Phone number must be at most 20 digits.'
        },
        (value: string) => {
          if (/[^0-9]/.test(value)) return 'Name can not contain characters.'
          return true
        },
      ]

      const putProfileSettings = async () => {
        // const valid: [boolean, string] = await phoneNumberRules()         //validation

        putSettings(state)
      }

      return {
        state,
        nameRules,
        phoneNumberRules,
      }
    },
  }
</script>
