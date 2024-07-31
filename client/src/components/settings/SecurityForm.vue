<template>
  <v-form>
    <v-text-field
      v-model="state.originalPassword"
      label="Password"
      required
      :rules="passwordRules"
    />

    <v-text-field
      v-model="state.confirmPassword"
      label="Confirm Password"
      required
      :rules="passwordRules"
    />

    <v-btn
      class="me-4"
      type="submit"
    >
      Change Password
    </v-btn>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { passwordRules } from '@/utilities/validators'

  type FormState = {
    originalPassword: string,
    confirmPassword: string,
  }

  export default {

    name: 'SecurityForm',
    setup () {
      const state = ref<FormState>(
        {
          originalPassword: '',
          confirmPassword: '',
        }
      )

      return {
        state,
        passwordRules,
      }
    },
  }
</script>
