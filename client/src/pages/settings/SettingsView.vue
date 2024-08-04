<template>
  <v-card>
    <v-card-title class="text-h3">
      Settings
    </v-card-title>
    <v-card-item>
      <v-btn-toggle
        divided
        variant="outlined"
      >
        <v-btn @click="profile = true">Profile Information</v-btn>

        <v-btn @click="profile = false">Security Information</v-btn>
      </v-btn-toggle>
    </v-card-item>
  </v-card>
  <v-card-item>
    <ProfileInformationForm v-if="profile" />
    <SecurityForm v-else />
  </v-card-item>
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
