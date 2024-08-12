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
                <v-col v-for="plan in testPlans" :key="plan.id" cols="12" sm="6" md="4">
                    <v-card class="ma-2" outlined>
                        <v-card-title @click="viewPlan(plan.id)">{{ plan.title }}</v-card-title>
                        <v-card-subtitle>
                            Created: {{ plan.created }}
                            Updated: {{ plan.modified }}
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
        const testPlans = ref([]);


        //PROJECCCCCT IIIIIIDDDD
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

        onMounted(() => {
        GetTestPlans();
        });


        return{
            count,
            SearchPlans,
            searchText,
            testPlans,
            GetTestPlans
        }
    }
}
</script>
