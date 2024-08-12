<template>
    <div style="margin-left: 7cm; margin-right: 7cm;">
        <v-container>
            <v-row >
                <p class="mt-2 text-h4 text-blue-darken-4" variant="h5">Test Plans</p>
                <v-spacer></v-spacer>
            </v-row>

            <v-row>
                <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">There are {{ count }} Test Plans</p>
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
                <v-card class="mx-auto" >
                    <v-card-title class="d-flex justify-space-between align-center">
                        {{ plan.title }}
                        <v-menu>
                            <template v-slot:activator="{ props }">
                            <v-btn icon="mdi-dots-vertical" v-bind="props" flat></v-btn>
                            </template>
                            <v-list>
                            <v-list-item @click="updatePlan(plan.id)" >
                                <v-list-item-title>Update</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="deletePlan(plan.id)">
                                <v-list-item-title>Delete</v-list-item-title>
                            </v-list-item>
                            </v-list>
                        </v-menu>
                    </v-card-title>
                    <v-card-subtitle>
                        <br>
                        <strong>  Created:</strong> {{ plan.created }}
                        <span class="mx-16"></span>
                        <strong>  Updated:</strong> {{ plan.modified }}
                    </v-card-subtitle>
                </v-card>
                </v-col>
            </v-row>

        </v-container>
    </div>
</template>

<script>
import axios from '@/api/axios';
import { onMounted } from 'vue';

export default{
    setup(){
        const count = ref(0);
        const searchText = ref('');
        // const testPlans = ref([]);
        const testPlans = ref([{id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'},
        {id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'},
        {id: '1',title: 'Plan A',created: '2024-08-01',modified: '2024-08-05'}
        ]);


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
            deletePlan
        }
    }
}
</script>
