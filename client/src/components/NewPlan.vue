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
                    <!-- <strong>Title</strong> -->
                    <v-text-field v-model="details.title" density="compact" placeholder="Title" variant="outlined"></v-text-field>
                <div>
                    <v-radio-group v-model="details.type">
                    <v-radio label="Create With Default Templates" value="template"></v-radio>
                    <v-radio label="Create With Custom Templates" value="blank" ></v-radio>
                    </v-radio-group>
                </div>
                </v-card-subtitle>
                <v-divider></v-divider>
                <v-card-actions>
                <v-btn  @click="dialog = false"  style="background-color: #37ADE3;" class="text-white" >Close</v-btn>
                <v-btn  style="background-color: #43A047;" class="text-white" @click="createTestPlan">Create</v-btn>
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
                await axios.CreateNewTestPlan(details.value,projectId);
            } catch(error){
                console.error(error);
            }
        }
        return{
            dialog,
            createTestPlan,
            details
        }

    }
}
</script>