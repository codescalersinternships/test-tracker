<template>
    <div class="text-center pa-4">
        <!-- this is just to be replaced later on with the + button on click , it opens the dialog.. -->
        <v-btn @click="dialog = true">
            Open Dialog
        </v-btn>
    
        <v-dialog v-model="dialog" max-width="600px">
        <v-card >
            <v-card-title>New Test Plan</v-card-title>
            <v-divider></v-divider>
            <br>
            <v-card-subtitle>
            <div>
                <strong>Title</strong>
                <v-text-field v-model="details.title" placeholder="Enter title "></v-text-field>
            </div>
            <div>
                <strong>Type</strong>
                <v-select v-model="details.type" :items="plans" label=" type"></v-select>
            </div>
            </v-card-subtitle>
            <v-divider></v-divider>
            <v-card-actions>
            <v-btn color="info" @click="dialog = false">Close</v-btn>
            <v-btn color="success" @click="createTestPlan">Create</v-btn>
            </v-card-actions>
        </v-card>
        </v-dialog>
    </div>
</template>

<script>
import axios from '@/api/axios';
export default{
    setup(){
        let dialog=ref(false);
        const details = ref({
        title: '',
        type: null,
        });

        const createTestPlan=async()=>{
            try{
                await axios.CreateNewTestPlan(details,projectId);
            } catch(error){
                console.error(error);
            }
        }


    }
}
</script>