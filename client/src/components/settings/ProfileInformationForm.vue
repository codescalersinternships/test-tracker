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
  import { defineComponent, ref } from 'vue'

  type FormState = {
    email: string,
    firstName: string,
    lastName: string,
    phoneNumber: string,
  }

  export default defineComponent({

    setup () {
      const state = ref<FormState>(
        {
          email: 'test@test.com',
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

      return {
        state,
        nameRules,
        phoneNumberRules,
      }
    },
  })
</script>
