<template>
  <div class="background pa-0">
    <v-container>
      <v-card
        class="ma-auto pa-12 pb-8"
        elevation="8"
        max-width="448"
        rounded="lg"
      >
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
            <v-typography class="mt-2 text-h5 text-grey-darken-2 font-weight-bold" variant="h5">Hello {{username}}</v-typography>
          </v-col>
        </v-row>


        <v-row>
          <v-col class="d-flex justify-center">
            <v-typography>
              <v-typography class="font-weight-bold text-grey-darken-3">@{{ invitor }}</v-typography>
              <v-typography class="text-grey-darken-3"> has invited you to join the </v-typography>
              <v-typography class="font-weight-bold text-grey-darken-3" >Test Tracker App</v-typography>
            </v-typography>
          </v-col>
        </v-row>


  
        <v-row>
          <v-col class="d-flex justify-center">
            <v-typography class="text-center text-grey-darken-3">
              Write your password to confirm your registration
            </v-typography>
          </v-col>
        </v-row>
  
        <v-row>
          <v-col>
            <v-text-field
              v-model="userPassword.password1"
              :append-inner-icon="visible1 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible1 ? 'password' : 'text'"
              density="compact"
              placeholder="Password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="visible1 = !visible1"
            ></v-text-field>
            <v-text-field
              v-model="userPassword.password2"
              :append-inner-icon="visible2 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible2 ? 'password' : 'text'"
              density="compact"
              placeholder="Re Password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="visible2 = !visible2"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col class="d-flex justify-center">
            <v-btn class="mb-8 w-100" color="primary" size="large" @click="RegisterUser">
              Register
            </v-btn>
          </v-col>
        </v-row>

        <v-divider></v-divider>
        <br>

        <v-row>
            <v-col class="d-flex justify-center">
            <a class="text-caption text-decoration-none text-grey-darken-2">Already have an account? 
                <a
                class="text-caption text-decoration-none text-blue"
                href="#"
                @click.prevent="LogIn"
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
import axios from '@/api/axios';
import { useRouter } from 'vue-router';

export default{
    setup(){

      const router=useRouter();

      const userPassword=ref({
      password1: "",
      password2: "",
      })

      let visible1 = ref(false);
      let visible2 = ref(false);

      const username=ref("");
      const invitor=ref("");

      function RegisterUser(){
        axios.SignUpInvitation(userPassword.value)
      }

      function LogIn(){
        router.push(`/`);
      }

      return{
          userPassword,
          visible1,
          visible2,
          RegisterUser,
          LogIn,
          username,
          invitor,
      }
    }
}
</script>