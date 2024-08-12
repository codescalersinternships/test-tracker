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
        <v-text-field v-model="searchText" label="Search" variant="outlined" />
        <v-btn color="primary" style="height: 56px; width:80px; padding: 0; margin: 0;" variant="outlined" @click="search">Search</v-btn>
      </v-row>

      <!-- seperate component for displaying members? -->

    </v-container>
  </div>
</template>

<script>
  import { defineProps, ref } from 'vue'
  import { searchProject } from '@/api/userservice'

  export default {
    setup () {
      const count = ref(2)

      const projectText = () => { if (count.value !== 1) { return 'There are ' + count.value + ' projects.' } return 'There is 1 project.' }

      const searchText = ref('')

      const search = async () => {
        try {
          projects.value = await searchProject(searchText.value)
        } catch (error) {
          console.error('Error searching for projects:', error)
        }
      }

      return {
        count,
        search,
        searchText,
        projectText,
      }
    },

  }
</script>
