<template>
  <v-form
    ref="form"
    fast-fail
    @submit.prevent
  >
    <v-text-field
      v-model="project.title"
      base-color="blue"
      clearable
      color="blue"
      label="Title"
      required
      :rules="titleRules"
    />

    <v-text-field
      v-model="project.short_description"
      base-color="blue"
      clearable
      color="blue"
      label="Description"
      required
      :rules="descriptionRules"
    />
    <v-switch
      v-model="githubRepo"
      base-color="blue"
      label="Github repository"
    />

    <v-text-field
      v-if="githubRepo"
      v-model="project.repo_link"
      clearable
      label="Git repository"
      :rules="githubRepoRules"
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
        @click="createProject"
      />
    </v-col>
  </v-form>
</template>

  <script lang="ts">
  import { ref } from 'vue'
  import { postProject } from '@/api/projectService'
  import { Project } from '@/types/types'
  import { descriptionRules, githubRepoRules, titleRules } from '@/utilities/validators'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProjectForm',
    setup () {
      const notifier = useNotifier('top right')

      const githubRepo = ref<boolean>(false)

      const form = ref()

      const loading = ref(false)

      const project = ref<Partial<Project>>(
        {
          title: '',
          short_description: '',
          repo_link: '',
        }
      )

      const createProject = async () => {
        loading.value = true
        let projectObject: Partial<Project> = {
          title: project.value.title,
          short_description: project.value.short_description,
        }
        if (project.value.repo_link !== '') {
          projectObject = {
            ...projectObject,
            repo_link: project.value.repo_link,
          }
        }
        postProject(projectObject)
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
            let description = 'Can not create project'
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
        loading,
        project,
        githubRepo,
        titleRules,
        descriptionRules,
        githubRepoRules,
        createProject,
      }
    },
  }
  </script>
