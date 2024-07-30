<template>
    <v-container>
        <v-row >
            <v-col>
                <h2>ALL MEMBERS</h2>
            </v-col>

            <v-col class="justify-end">
                <v-btn class="pink white--text" color="info" @click="addMember">
                INVITE MEMBERS
                </v-btn>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <h4>-There are {{ count }} members registered</h4>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <h4>Search Members</h4>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-text-field label="Search" />
            </v-col>
            <v-col>
                <v-btn color="primary" @click="search">Search</v-btn>
            </v-col>
        </v-row>
        <v-row>

            <!-- <v-card
                title="Search Members"
                flat
            >
                <template v-slot:text>
                <v-text-field
                    v-model="search"
                    label="Search"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    hide-details
                    single-line
                ></v-text-field>
                </template>

                <v-data-table
                :headers="headers"
                :items="desserts"
                :search="search"
                :show-current-page="false"
                ></v-data-table>
            </v-card> -->
        </v-row>
    </v-container>



</template>

<script>
import { ref } from 'vue';
import { defineProps } from 'vue';
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

        const addMember = () => {
        };

        const buttonHover =()=>{

        }

        return{
            props,
            addMember,
            buttonHover,
        }
    }
    
}
</script>