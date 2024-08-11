<template>
    <div class="text-center pa-4">
        <!-- to be removed, this is just to be replaced later on with the + button on click , it opens the dialog.. -->
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
                <v-text-field v-model="title" placeholder="Enter title "></v-text-field>
            </div>
            <div>
                <strong>Test Plan</strong>
                <v-select v-model="selectedPlan" :items="plans" label="Select Plan"></v-select>
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

<!-- /test_plan/{project_id}/      endpoint -->

<script>

export default{
    setup(){
        let dialog=ref(false);
        const title = ref('');
        const selectedPlan = ref(null);

        const plans = ["haha"];

        function createTestSuite(){

        }

        return {
        dialog,
        title,
        selectedPlan,
        plans,
        createTestSuite
        };
    }
}
</script>