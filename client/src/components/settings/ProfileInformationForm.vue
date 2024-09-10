<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="profile.email"
      base-color="blue"
      color="blue"
      :counter="10"
      disabled
      label="E-mail"
    />

    <v-text-field
      v-model="profile.first_name"
      base-color="blue"
      clearable
      color="blue"
      label="First Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="profile.last_name"
      base-color="blue"
      clearable
      color="blue"
      label="Last Name"
      required
      :rules="nameRules"
    />

    <v-text-field
      v-model="profile.phone"
      base-color="blue"
      clearable
      color="blue"
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

        try {
          const response = await putSettings(userProfile)
          notifier.notify({
            title: 'Success',
            description: response.data.message,
            showProgressBar: true,
            timeout: 7_000,
            type: 'success',
          })
        } catch (err: any) {
          let description = 'Can not update profile settings'
          if (err.response) {
            description = err.response.data.message
          }
          notifier.notify({
            title: 'Fail',
            description,
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
        } finally {
          form.value.reset()
          loading.value = false
        }
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

<style lang="scss" scoped>

  .vue3-notifier-container {
    top: 90px;
  }

</style>
