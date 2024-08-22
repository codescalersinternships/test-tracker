<template>
  <v-card
    class="mx-auto my-6 py-6"
    variant="outlined"
    width="70%"
  >
    <v-card-title
      class="mx-6 px-6 justify-lg-center align-md-center"
    >
      <h1>Settings</h1>
    </v-card-title>
    <v-card-subtitle
      class="d-flex justify-lg-center align-md-center"
    >
      <v-btn-toggle
        base-color="black"
        color="blue"
        divided
        size="x-large"
        variant="outlined"
      >
        <v-btn @click="profile = true">Profile Information</v-btn>

        <v-btn @click="profile = false">Security Information</v-btn>
      </v-btn-toggle>
    </v-card-subtitle>
    <v-card-item
      class="mx-6 px-6"
    >
      <ProfileInformationForm v-if="profile" />
      <SecurityForm v-else />
    </v-card-item>
  </v-card>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import ProfileInformationForm from '@/components/settings/ProfileInformationForm.vue'
  import SecurityForm from '@/components/settings/SecurityForm.vue'

  export default {

    name: 'SettingsView',
    components: {
      ProfileInformationForm,
      SecurityForm,
    },
    setup () {
      const profile = ref<boolean>(true)

      return {
        ProfileInformationForm,
        SecurityForm,
        profile,
      }
    },
  }
</script>

<style lang="scss" scoped>

h1 {
  font-size: 1.7rem;
}

</style>
