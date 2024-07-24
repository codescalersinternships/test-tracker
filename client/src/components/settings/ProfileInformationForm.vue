<template>
  <form>
    <v-text-field
      v-model="state.email"
      :counter="10"
      label="Name"
    />

    <v-text-field
      v-model="state.firstName"
      label="E-mail"
      required
    />

    <v-text-field
      v-model="state.phoneNumber"
      label="Phone Number"
      required
    />

    <v-btn
      class="me-4"
    >
      submit
    </v-btn>
  </form>
</template>

<script lang="ts" setup>
  import { reactive } from 'vue'

  const initialState = {
    email: '',
    firstName: '',
    lastName: '',
    phoneNumber: '',
  }

  const state = reactive({
    ...initialState,
  })

</script>
