<template>
    <div class="text-center pa-4">
        <!-- this is just to be replaced later on with the + button on click , it opens the dialog.. -->
        <v-btn @click="dialog = true">
            Open Dialog
        </v-btn>
    
        <v-dialog v-model="dialog" max-width="600px">
        <v-card >
            <v-card-title>New Test Suite</v-card-title>
            <v-divider></v-divider>
            <br>
            <v-card-subtitle>
            <div>
                <strong>Title</strong>
                <v-text-field v-model="details.title" placeholder="Enter title "></v-text-field>
            </div>
            <div>
                <strong>Test Plan</strong>
                <v-select v-model="details.test_plan" :items="plans" label="Select Plan"></v-select>
            </div>
            </v-card-subtitle>
            <v-divider></v-divider>
            <v-card-actions>
            <v-btn color="info" @click="dialog = false">Close</v-btn>
            <v-btn color="success" @click="createTestSuite">Create</v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from '@/api/axios';
import { onMounted } from 'vue';


export default{
    setup(){
        let dialog=ref(false);
        const details = ref({
        title: '',
        test_plan: null,
        });

        const plans = ref([]);

        //from where to get the project id???
        const fetchPlans = async () => {
            try {
            plans.value = await axios.GetPlans(projectId);
            } catch (error) {
            console.error(error);
            }
        };

        const createTestSuite=async()=>{
            try{
                await axios.CreateNewTestSuite(details,projectId);
            } catch(error){
                console.error(error);
            }
        }

        onMounted(() => {
        fetchPlans();
        });

        return {
        dialog,
        details,
        plans,
        createTestSuite,
        fetchPlans,
        };
    }
}
</script>