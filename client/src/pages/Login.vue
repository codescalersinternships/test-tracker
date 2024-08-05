<template>
    <div>
        <v-card
            class="mx-auto pa-12 pb-8"
            elevation="8"
            max-width="448"
            rounded="lg"
        >
        <v-row class="d-flex justify-center mb-4" no-gutters>
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
            <v-typography class="mt-2 text-h5" variant="h5">
            Welcome
          </v-typography>
        </v-col>
        </v-row>

        <v-row>
            <v-col class="d-flex justify-center">
                <v-typography class="text-center">
                    Sign in with your <v-typography class="font-weight-bold" variant="body-1">Test Tracker</v-typography> account
                </v-typography>
            </v-col>
        </v-row>

        <v-col>
            <v-row>
                <v-text-field
                v-model="userInfo.email"
                density="compact"
                placeholder="Email"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                ></v-text-field>
            </v-row>
            <v-row>
                <v-text-field
                v-model="userInfo.password"
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visible ? 'text' : 'password'"
                density="compact"
                placeholder="Password"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                @click:append-inner="visible = !visible"
                ></v-text-field>
            </v-row>
            <v-row>
                <v-col class="d-flex justify-end">
                <a
                    class="text-caption text-decoration-none text-grey"
                    href="#"
                    rel="noopener noreferrer"
                    target="_blank"
                >
                    Forgot Password?
                </a>
                </v-col>
            </v-row>
        </v-col>

        <v-btn
        class="mb-8"
        color="primary"
        size="large"
        variant="outlined"
        block
        @click="SumbitLogIn" 
        >
        Log In
        </v-btn>
        <v-divider></v-divider>
        <br>

        <v-row>
            <v-col cols="6" class="d-flex justify-center">
                <v-btn density="default" class="w-100" outlined color="black">
                    <v-icon left>mdi-github</v-icon>
                    Github
                </v-btn>
            </v-col>
            <v-col cols="6" class="d-flex justify-center">
                <v-btn density="default" class="w-100" outlined color="black">
                    TFT Connect
                </v-btn>
            </v-col>
        </v-row>
        <br>
        <v-divider></v-divider>
        <br>

        <v-row>
            <v-col class="d-flex justify-center">
            <a class="text-caption text-decoration-none text-grey">
                New to Test Tracker?
            </a>
            </v-col>
        </v-row>
        <br>
        <v-row>
        <v-col class="d-flex justify-center">
            <v-btn class="mb-8 w-100" color="primary" size="large">
                Create Account
            </v-btn>
        </v-col>
        </v-row>

      </v-card>
    </div>
  </template>

<style scoped>
.background {
  background: url('../assets/authPagesBackGround.png');
  background-size: cover;
  height: 100vh;
}
</style>


<script>
import axios from '../api/axios.ts';

export default{
    setup(){

        const userInfo=ref({
        email: "",
        password: "",
        })

        let visible = ref(false);

        function togglePasswordVisibility() {
        passwordVisible.value = !passwordVisible.value;
        }


        function SumbitLogIn(){
            axios.LogInUser(userInfo.value)//not connected
        }

        
        function SubmitLoginGithub(){
            axios.LogInGitHub();
        }

        return{
            SumbitLogIn,
            SubmitLoginGithub,
            userInfo,
        }
    }
}
</script>