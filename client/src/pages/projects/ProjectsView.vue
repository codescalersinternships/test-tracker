<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row class="mb-6">
        <v-typography class="mt-2 text-h4 text-blue" variant="h5">ALL PROJECTS</v-typography>
      </v-row>

      <v-row>
        <v-typography class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6"> {{ projectText() }} </v-typography>
      </v-row>
      <br>

      <v-row>
        <h4 class="mb-2">Search Projects</h4>
      </v-row>

      <v-row class="mb-6">
        <v-text-field
          append-inner-icon="mdi-magnify"
          density="compact"
          hide-details
          single-line
          variant="solo"
          @input="search"
        >
          <template #append-inner>
            <v-icon color="blue" />
          </template>
          <!-- I dont know why its not working, it was working with a butoon before -->
        </v-text-field>
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
                  <v-btn
                    color="white"
                    icon="mdi-dots-vertical"
                    size="large"
                    variant="text"
                  />
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text class="mx-4">{{ project.description }}</v-card-text>
            <v-btn
              append-icon="mdi-chevron-right"
              block
              color="blue"
              text="Open Project"
              variant="tonal"
            />
          </v-card>

        </v-col>
      </v-row>
      <v-row justify="center">
        <v-pagination
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
  import { ref } from 'vue'
  import { searchProject } from '@/api/userservice'
  import { useNotifier } from 'vue3-notifier'

  export default {

    name: 'ProjectsView',
    setup () {
      const notifier = useNotifier('bottom')

      const projects = ref<Project[]>()

      onMounted(() => {
        projects.value = getProjects()
      }
      )

      // [
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      //   {
      //     title: 'title',
      //     id: '1',
      //     description: 'project description',
      //   },
      // ]

      const searchText = ref('')

      const count = ref(projects.value.length)

      const projectText = () => {
        if (count.value !== 1) {
          return 'There are ' + count.value + ' projects.'
        }
        return 'There is 1 project.'
      }

      const search = async () => {
        const text = searchText.value
        searchProject(text)
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

      return {
        search,
        projects,
        searchText,
        projectText,
      }
    },

  }
</script>

<style lang="scss" scoped>
::v-deep .v-icon {
  color: #2196F3 !important;
}
</style>
