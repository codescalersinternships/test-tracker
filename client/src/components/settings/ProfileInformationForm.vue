<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="profile.password"
      :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      base-color="blue"
      color="blue"
      label="Old password"
      required
      :rules="oldPasswordRule"
      :type="showPassword ? 'text' : 'password'"
      @click:append-inner="showPassword = !showPassword"
    />
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
  import { nameRules, oldPasswordRule, phoneNumberRules } from '@/utilities/validators'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProfileInformationForm',
    setup () {
      const notifier = useNotifier('top right')

      const form = ref()

      const loading = ref(false)

      const profile = ref<UserProfile>(
        {
          email: '',
          first_name: '',
          last_name: '',
          phone: '',
          password: '',
        }
      )

      const showPassword = ref(false)

      const updateProfileSettings = async () => {
        loading.value = true
        const userProfile: Partial<UserProfile> = {
          first_name: profile.value.first_name,
          last_name: profile.value.last_name,
          phone: profile.value.phone,
          password: profile.value.password,
        }
        putSettings(userProfile)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: response.data.message,
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
            loading.value = false
          })
          .catch((err: any) => {
            let description = 'Can not update profile settings'
            if (err.response) {
              description = err.response.data.detail
            }
            notifier.notify({
              title: 'Fail',
              description,
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            loading.value = false
          })
      }

      return {
        form,
        profile,
        loading,
        nameRules,
        showPassword,
        oldPasswordRule,
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
