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
            <p class="mt-2 text-h5 text-grey-darken-2 font-weight-bold" variant="h5">Hello {{username}}</p>
          </v-col>
        </v-row>


        <v-row>
          <v-col class="d-flex justify-center">
            <p>
              <p class="font-weight-bold text-grey-darken-3">@{{ invitor }}</p>
              <p class="text-grey-darken-3"> has invited you to join the </p>
              <p class="font-weight-bold text-grey-darken-3" >Test Tracker App</p>
            </p>
          </v-col>
        </v-row>


  
        <v-row>
          <v-col class="d-flex justify-center">
            <p class="text-center text-grey-darken-3">
              Write your password to confirm your registration
            </p>
          </v-col>
        </v-row>
  
        <v-row>
          <v-col>
            <v-text-field
              v-model="userPassword.password1"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showPassword ? 'password' : 'text'"
              density="compact"
              placeholder="Password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="showPassword = !showPassword"
            ></v-text-field>
            <v-text-field
              v-model="userPassword.password2"
              :append-inner-icon="showRePassword ? 'mdi-eye-off' : 'mdi-eye'"
              :type="showRePassword ? 'password' : 'text'"
              density="compact"
              placeholder="Re Password"
              prepend-inner-icon="mdi-lock-outline"
              variant="outlined"
              @click:append-inner="showRePassword = !showRePassword"
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
import axios from '@/api/axios';
import { useRouter } from 'vue-router';
import AlreadyHaveAnAccount from '@/components/AlreadyHaveAnAccount.vue';

export default{
  components: {
    AlreadyHaveAnAccount,
  },
  setup(){

    const router=useRouter();

    const userPassword=ref({
    password1: "",
    password2: "",
    })

    let showPassword = ref(true);
    let showRePassword = ref(true);

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
        showPassword,
        showRePassword,
        RegisterUser,
        LogIn,
        username,
        invitor,
    }
  }
}
</script>