<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row>
        <v-typography class="mt-2 text-h4 text-blue" variant="h5">ALL PROJECTS</v-typography>
        <v-spacer />
      </v-row>

      <v-row>
        <v-typography class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6"> {{ projectText() }} </v-typography>
      </v-row>
      <br>

      <v-row>
        <h4 class="mb-2">Search Projects</h4>
      </v-row>

      <v-row>
        <v-text-field
          append-inner-icon="mdi-magnify"
          density="compact"
          hide-details
          single-line
          variant="solo"
          @click:append-inner="search"
        />
      </v-row>

      <v-row>

        <v-col
          v-for="project in projects"
          :key="project.id"
          cols="12"
          md="4"
          sm="6"
        >
          <v-card class="ma-2" outlined>
            <v-card-subtitle>{{ project.title }}</v-card-subtitle>
            <v-card-actions>
              <v-btn>View Details</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

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

      const projects = [
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
        {
          title: 'title',
          id: '1',
        },
      ]

      const searchText = ref('')

      const count = ref(projects.length)

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
