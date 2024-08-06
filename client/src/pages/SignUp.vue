<template>
    <div class="background pa-0">
        <v-container>
            <v-card
                class="ma-auto pa-12 pb-8"
                elevation="8"
                max-width="448"
                rounded="lg">
                <v-row class="d-flex justify-center" no-gutters>
                    <v-col class="d-flex justify-center" style="max-width: 100px; width: 100px;">
                        <v-img
                        src="@/assets/logo.png"
                        style="width: 100%; height: auto;"
                        contain
                        ></v-img>
                    </v-col>
                </v-row>

                <v-row class="d-flex justify-center mb-4" no-gutters>
                    <v-col class="d-flex justify-center" style="max-width: 80px; width: 80px;">
                        <v-typography class="mt-2 text-h5 text-grey-darken-2" variant="h5">Sign up</v-typography>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col>
                        <v-text-field
                        v-model="newUser.first_name"
                        density="compact"
                        placeholder="First Name"
                        prepend-inner-icon="mdi-account-outline"
                        variant="outlined"
                        ></v-text-field>
                        <v-text-field
                        v-model="newUser.last_name"
                        density="compact"
                        placeholder="Last Name"
                        prepend-inner-icon="mdi-account-outline"
                        variant="outlined"
                        ></v-text-field>
                        <v-text-field
                        v-model="newUser.email"
                        density="compact"
                        placeholder="Email"
                        prepend-inner-icon="mdi-email-outline"
                        variant="outlined"
                        ></v-text-field>
                        <v-text-field
                        v-model="newUser.password"
                        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                        :type="visible ? 'password' : 'text'"
                        density="compact"
                        placeholder="Password"
                        prepend-inner-icon="mdi-lock-outline"
                        variant="outlined"
                        @click:append-inner="visible = !visible"
                        ></v-text-field>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col class="d-flex justify-center">
                        <v-btn class="mb-8 w-100" color="primary" size="large">
                        Register
                        </v-btn>
                    </v-col>
                </v-row>

                <v-divider></v-divider>
                <br>
        
                <v-row>
                <v-col cols="6" class="d-flex justify-center">
                    <v-btn variant="outlined" class="w-100" @click="SubmitLoginGithub">
                    <v-icon left>mdi-github</v-icon>
                    Github
                    </v-btn>
                </v-col>
                <v-col cols="6" class="d-flex justify-center">
                    <v-btn variant="outlined" class="w-100">
                    <img src="@/assets/tflogo.png" width=12px>
                    TFT Connect
                    </v-btn>
                </v-col>
                </v-row>
        

                <br>
                <v-divider></v-divider>
                <br>

                <v-row>
                    <v-col class="d-flex justify-center">
                    <a class="text-caption text-decoration-none text-grey-darken-2">Already have an account? 
                        <a
                        class="text-caption text-decoration-none text-blue"
                        href="#"
                        rel="noopener noreferrer"
                        target="_blank"
                        >
                        Sign in
                        </a></a>
                    </v-col>
                </v-row>
            </v-card>
        </v-container>
    </div> 
</template>

<style scoped>
.background {
background: url('../assets/authPagesBackGround.png');
background-size: 100% 100%;
}
</style>

<script>
import axios from '../api/axios.ts';

export default{
    setup(){

        const newUser=ref({
        first_name: "",
        last_name: "",
        email:"",
        password:"",
        })

        let visible = ref(false);

        function RegisterNewUser(){
            axios.SignUp(newUser.value);
        }

        function SubmitLoginGithub(){
            axios.LogInGitHub();
        }


        return{
            RegisterNewUser,
            LogInGitHub,
            visible,
            newUser,
        }
    }
}
</script>