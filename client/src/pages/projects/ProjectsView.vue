<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row class="mb-6">
        <p class="mt-2 text-h4 text-blue" variant="h5">PROJECTS</p>
      </v-row>

      <v-row>
        <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6"> {{ projectText() }} </p>
      </v-row>
      <br>

      <v-row>
        <h4 class="mb-2">Search Projects</h4>
      </v-row>

      <v-row class="mb-6">
        <v-text-field
          v-model="searchText"
          append-inner-icon="mdi-magnify"
          density="compact"
          hide-details
          variant="solo"
          @input="search"
        />
      </v-row>

      <v-row class="mb-6">
        <v-col
          v-for="project in projects"
          :key="project.id"
          cols="auto"
          md="6"
          sm="6"
        >
          <v-card
            class="ma-auto"
          >
            <v-card-title>
              <v-row class="pa-4">
                <v-col
                  cols="11"
                >
                  {{ project.title }}
                </v-col>
                <v-col
                  cols="1"
                >
                  <v-icon icon="mdi-delete" style="color:red;" />
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text class="mx-4">{{ project.short_description }}</v-card-text>
            <v-btn
              append-icon="mdi-chevron-right"
              block
              color="blue"
              variant="tonal"
            >
              <RouterLink
                class="mx-3 pa-3 font-weight-black text-blue"
                :to="{ name: 'projectDetails', params: {projectId: project.id} }"
              >
                Open Project
              </RouterLink>
            </v-btn>
          </v-card>

        </v-col>
      </v-row>
      <v-row justify="center">
        <v-pagination
          v-if="count >= 4"
          v-model="page"
          color="blue"
          :length="4"
          rounded="circle"
        />
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
  import { ref, watch } from 'vue'
  import { getProjects, searchProject } from '@/api/ProjectService'
  import { useNotifier } from 'vue3-notifier'
  import { Project } from '@/types/types'
  import { RouterLink } from 'vue-router'

  export default {
    name: 'ProjectsView',

    setup () {
      const notifier = useNotifier('top right')

      const page = ref(1)

      const projects = ref<Project[]>([])

      const count = ref(5)

      const getPage = async (page: number) => {
        getProjects(page).then((response: any) => {
          projects.value = response.data.results
          // count.value = response.body.total_count
        })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not get projects',
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            console.error(err)
          })
      }

      onMounted(() => {
        getPage(page.value)
      })

      watch(page, (currentValue, oldValue) => {
        getPage(currentValue)
      })

      const searchText = ref('')

      const search = async () => {
        searchProject(searchText.value)
          .then((response: any) => {
          })
          .catch((err: any) => {
            notifier.notify({
              title: 'Fail',
              description: 'Can not search projects',
              showProgressBar: true,
              timeout: 7_000,
              type: 'error',
            })
            console.error(err)
          })
      }

      const projectText = () => {
        if (count.value !== 1) {
          return 'There are ' + count.value + ' projects.'
        }
        return 'There is 1 project.'
      }

      return {
        page,
        count,
        search,
        projects,
        searchText,
        projectText,
        RouterLink,
      }
    },

  }
</script>

<style lang="scss" scoped>
::v-deep .v-icon {
  color: #2196F3 !important;
}
a {
  text-decoration: none;
  color: inherit;
  font-size: 1rem;
}
.mdi-delete {
  width: 25px;
  height: 25px;
}
</style>
