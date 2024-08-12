<template>
    <v-row>
      <v-col class="d-flex justify-center">
        <a class="text-caption text-decoration-none text-grey-darken-2">
          Already have an account? 
          <a
            class="text-caption text-decoration-none text-blue"
            href="#"
            @click.prevent="handleLogIn"
          >
            Sign in
          </a>
        </a>
      </v-col>
    </v-row>
</template>

<script>
import { useRouter } from 'vue-router';

export default{
    setup(){
        const router = useRouter();
        function handleLogIn() {
            router.push(`/`);
        }

        return {
        handleLogIn,
        };
    }
}
</script>