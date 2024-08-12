<template>
    <v-btn variant="outlined" class="w-100" @click="SubmitLoginGithub">
        <v-icon left>mdi-github</v-icon>
        Github
    </v-btn>
</template>

<script>
import axios from '../api/axios.ts';
export default{
    setup(){
        function SubmitLoginGithub(){
        try{
            axios.LogInGitHub();
        }catch(error){
            console.error(error);
        }
        }

        return{
            SubmitLoginGithub
        }
    }
}
</script>