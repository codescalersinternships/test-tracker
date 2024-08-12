<template>
    <div style="margin-left: 7cm; margin-right: 7cm;">
        <v-container>
            <v-row >
                <v-typography class="mt-2 text-h4 text-blue-darken-4" variant="h5">ALL MEMBERS</v-typography>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="addMember">
                    INVITE MEMBERS
                </v-btn>
            </v-row>

            <v-row>
                <v-typography class="mt-2 text-h6 text-grey-darken-2 mb-8" variant="h6">-There are {{ count }} members registered</v-typography>
            </v-row>
            <br>

            <v-row>
                <h4  class="mb-2">Search Members</h4>
            </v-row>

            <v-row>
                <v-text-field v-model="searchText" label="Search" variant="outlined"></v-text-field>
                <v-btn color="primary" variant="outlined" @click="SearchMember"  style="height: 56px; width:80px; padding: 0; margin: 0;">Search</v-btn>
            </v-row>

                    <!-- seperate component for displaying members? -->
            <v-row>
                <v-col v-for="member in members" :key="member.email" cols="12" sm="6" md="4">
                    <v-card class="ma-2" outlined>
                        <!-- <v-card-title>{{ member.full_name }}</v-card-title> -->
                        <v-card-subtitle>{{ member.full_name }}</v-card-subtitle>
                        <v-card-actions>
                        <v-btn @click="viewMember(member.id)">View Details</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
        </v-row>
        </v-container>
    </div>
</template>

<script>
import { ref } from 'vue';
import { defineProps } from 'vue';
import axios from '@/api/axios';
export default{
    setup(){
        const props =defineProps({
            count:{
                type :Number,
                required : true,
            },
            members:{
                type :Array,
                required :true, 
            },
        });


        let searchText=ref("");

        const addMember = () => {
        };

        const SearchMember = async () => {
            try {
               members.value= await axios.Search(searchText.value);
            } catch (error) {
                console.error(error);
            }
        };

        return{
            props,
            SearchMember,
            addMember,
            searchText
        }
    }
    
}
</script>