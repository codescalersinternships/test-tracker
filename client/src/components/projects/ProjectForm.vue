<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="state.title"
      clearable
      label="Title"
      required
      :rules="titleRules"
    />

    <v-text-field
      v-model="state.Description"
      clearable
      label="Description"
      required
      :rules="descriptionRules"
    />
    <v-switch
      v-model="githubRepo"
      label="Github repository"
    />

    <v-text-field
      v-if="githubRepo"
      v-model="state.githubRepo"
      clearable
      label="Github repository"
      :rules="githubRepoRules"
    />

    <v-btn
      block
      class="me-4"
      :disabled="!form?.isValid"
      text="Submit"
      type="submit"

      @click="createProject"
    />
  </v-form>
</template>

  <script lang="ts">
  import { ref } from 'vue'
  import { postProject } from '@/api/userservice'
  import { Project } from '@/types/types'
  import { descriptionRules, githubRepoRules, titleRules } from '@/utilities/validators'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProjectForm',
    setup () {
      const notifier = useNotifier('bottom')

      const githubRepo = ref<boolean>(false)

      const form = ref()

      const state = ref<Project>(
        {
          title: '',
          description: '',
          githubRepo: '',
        }
      )

      const createProject = async () => {
        postProject(state.value)
          .then((response: any) => {
            notifier.notify({
              title: 'Success',
              description: 'Project created Successfully',
              showProgressBar: true,
              timeout: 7_000,
              type: 'success',
            })
          })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not create project',
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            console.error(err)
          })
      }

      return {
        form,
        state,
        githubRepo,
        titleRules,
        descriptionRules,
        githubRepoRules,
        createProject,
      }
    },
  }
  </script>
