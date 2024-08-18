<template>
    <div style="margin-left: 7cm; margin-right: 7cm;">
        <v-container>
            <v-row >
                <p class="mt-2 text-h4 text-blue-darken-4" variant="h5">Test Suites</p>
                <v-spacer></v-spacer>
            </v-row>

            <v-row>
                <p class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">There are {{ count }} Test Suite</p>
            </v-row>
            <br>

            <v-row>
                <h4  class="mb-2">Search Suites</h4>
            </v-row>

            <v-row>
                <v-text-field v-model="searchText" label="Search" variant="outlined"></v-text-field>
                <v-btn color="primary" variant="outlined" @click="SearchSuite"  style="height: 56px; width:80px; padding: 0; margin: 0;">Search</v-btn>
            </v-row>

            <v-row>
                <v-col v-for="suite in testSuites" :key="suite.id" cols="12" sm="6" md="4">
                    <v-card class="ma-2" outlined>
                        <v-card-title @click="viewSuite(suite.id)">{{ suite.title }}</v-card-title>
                        <v-card-subtitle>
                            Created: {{ suite.created }}
                            Updated: {{ suite.modified }}
                            Number of Test Cases: {{ suite.number_of_test_cases }}
                        </v-card-subtitle>
                        <v-card-actions>
                        </v-card-actions>
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
        //projectid testsuite .count
        const count = ref(0);
        const searchText = ref('');
        const testSuites = ref([]);

        const SearchSuite = async () => {
            try {
                testSuites.value=await axios.SearchSuite(projectId,searchText)
            } catch (error) {
                console.error(error);
            }
        };

        //from where to get the project id?
        const getSuites = async () => {
            try {
                testSuites.value=await axios.GetTestSuites(projectId)
            } catch (error) {
                console.error(error);
            }
        };

        onMounted(() => {
        getSuites();
        });

        return{
            count,
            searchText,
            testSuites,
            getSuites,
            SearchSuite
        }
    }
}
</script>