<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row>
        <p class="mt-2 text-h4 text-blue-darken-4" variant="h5">ALL MEMBERS</p>
        <v-spacer />
        <v-btn
          color="primary"
          @click="addMemberDialog=true"
        >
          INVITE MEMBERS
        </v-btn>
      </v-row>

      <v-dialog v-model="addMemberDialog" max-width="600px">
        <v-card>
          <v-form>
            <v-card-title>
              <br>
              <v-divider />
            </v-card-title>
            <v-card-text>
              <v-text-field
                v-model="inviteNewMember.first_name"
                density="compact"
                placeholder="First Name"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
              />
              <v-text-field
                v-model="inviteNewMember.last_name"
                density="compact"
                placeholder="Last Name"
                prepend-inner-icon="mdi-account-outline"
                variant="outlined"
              />
              <v-text-field
                v-model="inviteNewMember.email"
                density="compact"
                placeholder="Email"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
              />
              <p>Permission</p>
              <v-select
                :items="['Full access', 'Admin access']"
                label="Select"
              />
              <v-divider />
              <v-card-actions>
                <v-spacer />
                <v-btn color="info" @click="addMemberDialog = false">Close</v-btn>
                <v-btn color="success" :disabled="loadingAdd" :loading="loadingAdd" @click="addMember">ADD+</v-btn>
              </v-card-actions>
            </v-card-text>
          </v-form>
        </v-card>
      </v-dialog>

      <v-row>
        <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">There are {{ count }} members registered</p>
      </v-row>
      <br>

      <v-row>
        <h4 class="mb-2">Search Members</h4>
      </v-row>

      <v-row>
        <v-text-field v-model="searchText" label="Search" variant="outlined" />
        <v-btn color="primary" style="height: 56px; width:80px; padding: 0; margin: 0;" variant="outlined" @click="SearchMember">Search</v-btn>
      </v-row>

      <v-row>
        <v-col
          v-for="member in members"
          :key="member.email"
          cols="12"
          md="4"
          sm="6"
        >
          <v-card class="ma-2" outlined>
            <!-- implement viewMember -->
            <v-card-subtitle>{{ member.full_name }}</v-card-subtitle>
            <v-card-actions>
              <v-btn @click="viewMember(member.id)">View Details</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
  import { defineProps, ref } from 'vue'
  import axios from '@/api/axios'

  export default {
    setup () {
      const props = defineProps({
        count: {
          type: Number,
          required: true,
        },
        members: {
          type: Array,
          required: true,
        },
        project_id: {
          type: string,
          required: true,
        },
      })

      const inviteNewMember = ref({
        first_name: '',
        last_name: '',
        email: '',
      })

      const addMemberDialog = ref(false)

      const searchText = ref('')

      const loadingAdd = ref(false)

      const addMember = () => {
        loadingAdd.value = true
        try {
          notifier.notify({
            title: 'success',
            description: 'member added successfully',
            showProgressBar: true,
            timeout: 7_000,
            type: 'success',
          })
        } catch (error) {
          console.error(error)
          notifier.notify({
            title: 'Fail',
            description: 'cannot add member',
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
        } finally {
          loadingAdd.value = false
        }
      }

      const SearchMember = async () => {
        try {
          members.value = await axios.Search(searchText.value)
        } catch (error) {
          console.error(error)
          notifier.notify({
            title: 'Fail',
            description: 'no member found',
            showProgressBar: true,
            timeout: 7_000,
            type: 'error',
          })
        }
      }

      async function getMembers () {
        try {
          members = await axios.getProjectMembers(project_id)
        } catch (error) {
          console.error(error)
        }
      }

      onMounted(() => {
        getMembers()
      })

      return {
        props,
        SearchMember,
        searchText,
        inviteNewMember,
        addMemberDialog,
        addMember,
        loadingAdd,
      }
    },

  }
</script>
