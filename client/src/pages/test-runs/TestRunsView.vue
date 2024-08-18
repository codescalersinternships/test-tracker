<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row class="mb-6">
        <p class="mt-2 text-h4 text-blue" variant="h5">Test Runs</p>
      </v-row>

      <v-row>
        <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6"> {{ TestRunText() }} </p>
      </v-row>
      <br>

      <v-row>
        <h4 class="mb-2">Search Test Runs</h4>
      </v-row>

      <v-row class="mb-6">
        <v-column>
          <v-combobox
            :items="members"
            label="User Involved"
            variant="solo-filled"
          />
        </v-column>
        <v-column>
          <v-combobox
            :items="['Not Started', 'In Progress', 'Completed']"
            label="Status"
            variant="solo-filled"
          />
        </v-column>
        <v-column>
          <v-btn
            color="blue"
            text="Search"
            variant="tonal"
          />
        </v-column>
      </v-row>

      <v-row class="mb-6">
        <v-btn-toggle
          divided
          variant="outlined"
        >
          <v-btn @click="profile = true">Profile Information</v-btn>

          <v-btn @click="profile = false">Security Information</v-btn>
        </v-btn-toggle>
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
                    icon="mdi-delete"
                    size="large"
                    variant="text"
                  />
                </v-col>
              </v-row>
            </v-card-title>
            <v-card-text class="mx-4">{{ project.short_description }}</v-card-text>
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
  import { getProjects, searchProject } from '@/api/userservice'
  import { useNotifier } from 'vue3-notifier'
  import { TestRun } from '@/types/types'

  export default {

    name: 'TestRunsView',
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

      const TestRunText = () => {
        if (count.value !== 1) {
          return 'There are ' + count.value + ' test runs.'
        }
        return 'There is 1 test run.'
      }

      return {
        page,
        count,
        search,
        projects,
        members,
        TestRunText,
      }
    },

  }
  </script>

  <style lang="scss" scoped>
  ::v-deep .v-icon {
    color: #2196F3 !important;
  }
  </style>
