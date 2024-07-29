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
        <v-btn @click="update">Profile Information</v-btn>

        <v-btn @click="update">Security Information</v-btn>
      </v-btn-toggle>
    </v-card-item>
  </v-card>
  <v-card-item>
    <ProfileInformationForm v-if="profile" />
    <SecurityForm v-else />
  </v-card-item>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue'
  import ProfileInformationForm from '@/components/settings/ProfileInformationForm.vue'
  import SecurityForm from '@/components/settings/SecurityForm.vue'

  export default defineComponent({

    setup () {
      const profile = ref<boolean>(true)

      function update () {
        console.log(profile)
        profile.value = !profile.value
      }

      return {
        ProfileInformationForm,
        SecurityForm,
        update,
        profile,
      }
    },
  })
</script>
