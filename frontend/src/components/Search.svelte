<script>
    import { createEventDispatcher } from 'svelte';
    import axios from "../healpers/axios";

    export let objects; // [objects] is the array of objects to update with the new data
    export let objectsCopy; // [objectsCopy] is a copy of the objects array
    export let request; // [request] for the endpoint

    const dispatch = createEventDispatcher();
    let searchInput;
    
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    async function searchFunction(){
        const word = searchInput.value;
        if(word.length > 0){
            const response = await axios.get(
                `${request}${word}/`,config
            )
            objects = response.data.data
        }else{
            objects = objectsCopy
        }
        dispatch('message', {
            objects: objects
        });
    }

</script>

<div class="input-group">
    <input bind:this={searchInput} type="search" class="form-control rounded" placeholder="Search"
    aria-label="Search" aria-describedby="search-addon" />
    <button type="button" class="btn btn-outline-primary" 
        on:click={searchFunction}>
        Search
    </button>
</div>
