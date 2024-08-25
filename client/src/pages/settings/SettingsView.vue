<template>
  <div
    class="settings"
  >
    <v-card
      class="mx-auto py-6"
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
        <v-tabs
          v-model="tab"
          base-color="black"
          color="blue"
          size="x-large"
          variant="outlined"
        >
          <v-tab text="Profile Information" value="profile" />

          <v-tab text="Security Information" value="security" />
        </v-tabs>
      </v-card-subtitle>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="profile">
          <v-card-item
            class="mx-6 px-6"
          >
            <ProfileInformationForm />
          </v-card-item>
        </v-tabs-window-item>
        <v-tabs-window-item value="security">
          <v-card-item
            class="mx-6 px-6"
          >
            <SecurityForm />
          </v-card-item>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card>
  </div>
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
      const tab = ref('profile')

      return {
        ProfileInformationForm,
        SecurityForm,
        tab,
      }
    },
  }
</script>

<style lang="scss" scoped>

h1 {
  font-size: 1.7rem;
}

.settings {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

</style>
