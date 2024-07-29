<template>
  <v-form>
    <v-text-field
      v-model="state.originalPassword"
      label="Password"
      required
      :rules="originalPasswordRules"
    />

    <v-text-field
      v-model="state.confirmPassword"
      label="Confirm Password"
      required
      :rules="confirmPasswordRules"
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
  import { defineComponent, ref } from 'vue'

  type FormState = {
    originalPassword: string,
    confirmPassword: string,
  }

  export default defineComponent({

    setup () {
      const state = ref<FormState>(
        {
          originalPassword: '',
          confirmPassword: '',
        }
      )

      const originalPasswordRules = [
        (value: string) => {
          if (value?.length > 1) return true
          return 'Password must be at least 1 character.'
        },
        (value: string) => {
          if (value?.length < 129) return true
          return 'Password must be at most 128 characters.'
        },
      ]

      const confirmPasswordRules = [
        (value: string) => {
          if (value?.length > 1) return true
          return 'Password must be at least 1 character.'
        },
        (value: string) => {
          if (value?.length < 129) return true
          return 'Password must be at most 128 characters.'
        },
        (value: string) => {
          if (value === state.value.originalPassword) return true
          return 'Passwords must match.'
        },
      ]

      return {
        state,
        originalPasswordRules,
        confirmPasswordRules,
      }
    },
  })
</script>
