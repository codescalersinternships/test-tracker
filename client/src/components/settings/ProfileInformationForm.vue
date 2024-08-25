<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="profile.email"
      :counter="10"
      disabled
      label="E-mail"
    />

    <v-text-field
      v-model="profile.first_name"
      clearable
      label="First Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="profile.last_name"
      clearable
      label="Last Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="profile.phone"
      clearable
      label="Phone Number"
      :rules="phoneNumberRules"
    />

    <v-col class="text-right">
      <v-btn
        class="me-4"
        color="blue"
        :disabled="!form?.isValid || loading"
        :loading="loading"
        size="large"
        text="Submit"
        type="submit"

        @click="updateProfileSettings"
      />
    </v-col>
  </v-form>
</template>

<script lang="ts">
  import { ref } from 'vue'
  import { putSettings } from '@/api/userService'
  import { UserProfile } from '../../types/types'
  import { nameRules, phoneNumberRules } from '@/utilities/validators'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProfileInformationForm',
    setup () {
      const notifier = useNotifier('top right')

      const form = ref()

      const loading = ref(false)

      const profile = ref<Partial<UserProfile>>(
        {
          email: '',
          first_name: '',
          last_name: '',
          phone: '',
        }
      )

      const updateProfileSettings = async () => {
        loading.value = true
        const userProfile: Partial<UserProfile> = {
          first_name: profile.value.first_name,
          last_name: profile.value.last_name,
          phone: profile.value.phone,
        }
        putSettings(userProfile)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: 'Profile changed Successfully',
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
            loading.value = false
          })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not change profile',
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            console.error(err)
            loading.value = false
          })
      }

      return {
        form,
        profile,
        loading,
        nameRules,
        phoneNumberRules,
        updateProfileSettings,
      }
    },
  }
</script>
