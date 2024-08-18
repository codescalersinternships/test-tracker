<template>
  <div class="text-center pa-4">
    <!-- this is just to be replaced later on with the + button on click , it opens the dialog.. -->
    <v-btn @click="dialog = true">
      Open Dialog
    </v-btn>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>New Test Plan</v-card-title>
        <v-divider />
        <br>
        <v-card-subtitle>
          <!-- <strong>Title</strong> -->
          <v-text-field v-model="details.title" density="compact" placeholder="Title" variant="outlined" />
          <div>
            <v-radio-group v-model="details.type">
              <v-radio label="Create With Default Templates" value="template" />
              <v-radio label="Create With Custom Templates" value="blank" />
            </v-radio-group>
          </div>
        </v-card-subtitle>
        <v-divider />
        <v-card-actions>
          <v-btn class="text-white" style="background-color: #37ADE3;" @click="dialog = false">Close</v-btn>
          <v-btn
            class="text-white"
            :disabled="loading"
            :loading="loading"
            style="background-color: #43A047;"
            @click="createTestPlan"
          >Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import axios from '@/api/axios'
  export default {
    setup () {
      const dialog = ref(false)
      const details = ref({
        title: '',
        type: null,
      })

      const loading = ref(false)

      const createTestPlan = async () => {
        loading.value = true
        try {
          await axios.CreateNewTestPlan(details.value, projectId)
          notifier.notify({
            title: 'Success',
            description: 'plan created successfully',
            showProgressBar: true,
            timeout: 7_000,
            type: 'success',
          })
        } catch (error) {
          console.error(error)
          notifier.notify({
            title: 'Fail',
            description: 'Failed to create plan',
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
        } finally {
          loading.value = false
        }
      }
      return {
        dialog,
        createTestPlan,
        details,
        loading,
      }
    },
  }
</script>
