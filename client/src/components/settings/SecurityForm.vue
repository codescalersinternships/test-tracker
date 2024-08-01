<template>
  <v-form>
    <v-text-field
      v-model="state.originalPassword"
      label="Password"
      required
      :rules="passwordRules"
      type="password"
    />

    <v-text-field
      v-model="state.confirmPassword"
      label="Confirm Password"
      required
      :rules="passwordRules"
      type="password"
    />

    <v-btn
      class="me-4"
      type="submit"
      @click="putProfileSettings"
    >
      Change Password
    </v-btn>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { passwordRules } from '@/utilities/validators'
  import { putSettings } from '@/api/axios'

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

      const done = ref<boolean>(false)

      const putProfileSettings = async () => {
        putSettings(state.value.originalPassword)
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
        passwordRules,
        putProfileSettings,
      }
    },
  }
</script>
