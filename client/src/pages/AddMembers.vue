<template>
  <div style="margin-left: 7cm; margin-right: 7cm;">
    <v-container>
      <v-row>
        <p class="mt-2 text-h4 text-blue-darken-4" variant="h5">All members</p>
        <v-spacer />
        <v-btn
          color="primary"
          @click="addMemberDialog=true"
        >
          Invite member
        </v-btn>
      </v-row>

      <v-dialog v-model="addMemberDialog" max-width="600px">
        <v-card>
          <v-form ref="form">
            <v-card-title>
              <br>
              <v-divider />
            </v-card-title>
            <v-card-text>
              <v-text-field
                v-model="inviteMember.first_name"
                density="compact"
                placeholder="First Name"
                prepend-inner-icon="mdi-account-outline"
                :rules="nameRules"
                variant="outlined"
              />
              <v-text-field
                v-model="inviteMember.last_name"
                density="compact"
                placeholder="Last Name"
                prepend-inner-icon="mdi-account-outline"
                :rules="nameRules"
                variant="outlined"
              />
              <v-text-field
                v-model="inviteMember.email"
                density="compact"
                placeholder="Email"
                prepend-inner-icon="mdi-email-outline"
                :rules="emailRules"
                variant="outlined"
              />
              <p>Permission</p>
              <v-select
                v-model="selectedPermission"
                :items="['Full access', 'Admin access']"
                label="Permission"
                @change="updatePermission"
              />
              <v-divider />
              <v-card-actions>
                <v-spacer />
                <v-btn color="info" @click="addMemberDialog = false">Close</v-btn>
                <v-btn color="success" :disabled="loadingAdd||!isFormValid" :loading="loadingAdd" @click="AddMember">ADD+</v-btn>
              </v-card-actions>
            </v-card-text>
          </v-form>
        </v-card>
      </v-dialog>

      <v-row>
        <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">There are {{ MembersCount }} members registered</p>
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
            <!-- implement viewMember and the display -->
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

<script lang="ts">
  import { ref } from 'vue'
  import api from '@/api/members'
  import { emailRules, nameRules } from '@/utilities/validators'
  import { inviteNewMember } from '@/types/types'

  export default {
    setup () {
      // const props = defineProps({
      //   count: {
      //     type: Number,
      //     required: true,
      //   },
      //   members: {
      //     type: Array,
      //     required: true,
      //   },
      // })
      const selectedPermission = ref < string >('Full access')
      const inviteMember = ref < inviteNewMember >({
        first_name: '',
        last_name: '',
        email: '',
        permission: 'full_access',
      })

      const addMemberDialog = ref(false)

      const members = ref([])
      const MembersCount = computed(() => members.value.length)

      const searchText = ref('')

      const loadingAdd = ref(false)

      async function AddMember () {
        try {
          await api.addMember(inviteMember.value)
          // description from the backend
          // notifier.notify({
          //   title: 'success',
          //   description: 'member added successfully',
          //   showProgressBar: true,
          //   timeout: 7_000,
          //   type: 'success',
          // })
        } catch (error) {
          console.error(error)
          // description from the backend
          // notifier.notify({
          //   title: 'Fail',
          //   description: 'cannot add member',
          //   showProgressBar: true,
          //   timeout: 7_000,
          //   type: 'error',
          // })
        } finally {
          loadingAdd.value = false
        }
      }
      const form = ref(null)

      const isFormValid = computed(() => form.value ? (form.value as any).isValid : false)

      const SearchMember = async () => {
        try {
          const response = await api.search(searchText.value)
          members.value = response.data
        } catch (error) {
          console.error(error)
          // description from the backend
          // notifier.notify({
          //   title: 'Fail',
          //   description: 'no member found',
          //   showProgressBar: true,
          //   timeout: 7_000,
          //   type: 'error',
          // })
        }
      }

      async function GetMembers () {
        try {
          const response = await api.getMembers()
          members.value = response.data
        } catch (error) {
          console.error(error)
        }
      }

      const updatePermission = () => {
        inviteMember.value.permission = selectedPermission.value === 'Full access' ? 'full_access' : 'admin_access'
      }

      onMounted(() => {
        GetMembers()
      })

      return {
        SearchMember,
        searchText,
        inviteMember,
        addMemberDialog,
        AddMember,
        loadingAdd,
        GetMembers,
        emailRules,
        nameRules,
        isFormValid,
        form,
        selectedPermission,
        updatePermission,
        MembersCount,
        members,
      }
    },
  }
</script>
