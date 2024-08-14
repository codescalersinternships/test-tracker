<template>
    <div style="margin-left: 7cm; margin-right: 7cm;">
        <v-container>
            <v-row >
                <p class="mt-2 text-h4 text-primary" variant="h5">Test Plans</p>
                <v-spacer></v-spacer>
            </v-row>

            <v-row>
                <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">There are <strong class="text-primary">{{ count }} </strong> Test Plans</p>
            </v-row>
            <br>

            <v-row>
                <h4  class="mb-2">Search Plans</h4>
            </v-row>

            <v-row>
                <v-text-field v-model="searchText" label="Search" variant="outlined"></v-text-field>
                <v-btn color="primary" variant="outlined" @click="SearchPlans"  style="height: 56px; width:80px; padding: 0; margin: 0;">Search</v-btn>
            </v-row>
            <!-- viewplan and viewsuite to be added later -->
            <v-row>
                <v-col v-for="plan in testPlans" :key="plan.id" cols="12">
                    <v-card class="mx-auto mb-4">
                        <v-card-item>
                            <v-card-title >
                            <span class="text-h5 font-weight-bold text-primary mr-6">{{ plan.title }}</span>
                            <v-icon  size="small" @click="updatePlan(plan.id)" >mdi-pencil</v-icon>
                            <!-- <v-menu>
                                <template v-slot:activator="{ props }">
                                <v-btn icon="mdi-dots-vertical" v-bind="props" flat></v-btn>
                                </template>
                                <v-list>
                                <v-list-item @click="updatePlan(plan.id)" class="mb-2">
                                    <v-list-item-title class="text-h5">Edit </v-list-item-title>
                                </v-list-item>
                                <v-list-item @click="deletePlan(plan.id)">
                                    <v-list-item-title class="text-h5"> Delete</v-list-item-title>
                                </v-list-item>
                                </v-list>
                            </v-menu> -->
                            </v-card-title>
                            <v-card-text>
                                <br>
                            </v-card-text>
                            <v-card-actions>
                                <p class="text-subtitle-1">
                                    Created:<strong> {{ plan.created }}  </strong>
                                    <span class="mx-16"></span>
                                    Updated:<strong> {{ plan.modified }}</strong>
                                </p>
                                <v-spacer></v-spacer>
                                <v-icon @click="openDeleteDialog(plan)" style="color: #E53935;">mdi-trash-can</v-icon>
                            </v-card-actions>
                        </v-card-item>
                    </v-card>
                </v-col>
            </v-row>

            <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                    <v-card-title class="headline">You are about to delete <span class="text-red-darken-1">{{ planToDelete.title }}</span></v-card-title>
                    <v-card-text>
                        <span class="text-red-darken-1">*</span>Please note that this action cannot be undone.
                        <v-divider></v-divider>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="dialogDelete = false">Cancel</v-btn>
                        <v-btn color="red" @click="deletePlan(planToDelete.id)">Delete</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

        </v-container>
    </div>
</template>

<script>
import axios from '@/api/axios';
import { onMounted } from 'vue';

export default{
    setup(){
        const searchText = ref('');
        // const testPlans = ref([]);
        const testPlans = ref([{id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'},
                            {id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'},
                            {id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'}
        ]);

        const count = ref(testPlans.value.length);
        const planToDelete = ref(null);
        const dialogDelete=ref(false);


        function openDeleteDialog(plan) {
            planToDelete.value = plan;
            dialogDelete.value = true;
        }


        //PROJECCCCCT IIIIIIDDDD????????????
        const SearchPlans = async () => {
            try {
                testPlans.value=await axios.SearchPlans(projectId,searchText)
            } catch (error) {
                console.error(error);
            }
        };

        const GetTestPlans = async () => {
            try {
                testPlans.value=await axios.GetPlans(projectId)
            } catch (error) {
                console.error(error);
            }
        };

        function updatePlan(planId){
            //open the create pop up with the create details, allowing edits?
        }

        async function deletePlan(planId){
            try {
                await axios.DeletePlan(projectId,planId);
            } catch (error) {
                console.error(error);
            }
        }

        onMounted(() => {
        GetTestPlans();
        });


        return{
            count,
            SearchPlans,
            searchText,
            testPlans,
            GetTestPlans,
            updatePlan,
            deletePlan,
            planToDelete,
            dialogDelete,
            openDeleteDialog,
        }
    }
}
</script>
