<template>
  <h1>Settings</h1>
  <v-card>
    <v-card-title>
      <v-btn-toggle
        divided
        variant="outlined"
      >
        <v-btn @click="profile = true">Profile Information</v-btn>

        <v-btn @click="profile = false">Security Information</v-btn>
      </v-btn-toggle>
    </v-card-title>
    <v-card-item>
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
  margin: 55px;
}

.main-card {
  margin: auto;
  width: 95%;
}

.v-card {
  width: 50%;
  margin: auto;
}

.v-card-title {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
