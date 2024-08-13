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

                <v-row class="d-flex justify-center" no-gutters>
                    <v-col class="d-flex justify-center" style="max-width: 80px; width: 80px;">
                        <p class="mt-2 text-h5 text-grey-darken-2" variant="h5">Sign up</p>
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
                    <LoginGithub/>
                </v-col>
                <v-col cols="6" class="d-flex justify-center">
                    <LoginTFT/>
                </v-col>
                </v-row>
        

                <br>
                <v-divider></v-divider>
                <br>

                <AlreadyHaveAnAccount/>

            </v-card>
        </v-container>
    </div> 
</template>

<style>
.background {
background-image: url('@/assets/authPagesBackGround.png');
background-size: cover;
background-position: center;
background-repeat: no-repeat;
padding: 0px;
margin: 0px;
width: 100%;
height: 100%;
}
</style>

<script>
import LoginGithub from '@/components/LoginGithub.vue';
import axios from '../api/axios.ts';
import AlreadyHaveAnAccount from '@/components/AlreadyHaveAnAccount.vue';
import LoginTFT from '@/components/LoginTFT.vue';

export default{
    components: {
    AlreadyHaveAnAccount,
    LoginGithub,
    LoginTFT
    },
    setup(){

        const newUser=ref({
        first_name: "",
        last_name: "",
        email:"",
        password:"",
        })

        let visible = ref(true);

        function RegisterNewUser(){
            try{
                axios.SignUp(newUser.value);
            }catch(error){
                console.error(error);
            }
        }

        return{
            RegisterNewUser,
            visible,
            newUser,
        }
    }
}
</script>