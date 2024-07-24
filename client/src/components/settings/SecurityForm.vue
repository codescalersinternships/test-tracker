<template>
  <form>
    <v-text-field
      v-model="state.password"
      label="Password"
      required
    />

    <v-text-field
      v-model="state.confirmPassword"
      label="Confirm Password"
      required
    />

    <v-btn
      class="me-4"
    >
      Change Password
    </v-btn>
  </form>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue'

  const initialState = {
    password: '',
    confirmPassword: '',
  }

  const state = reactive({
    ...initialState,
  })

</script>
