<script>
    import { onMount } from 'svelte';
    import axios from '../../healpers/axios';

    let lengthOfProjects = {};
    
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const lengthOfTotalProjects = await axios.get('/dashboard/total_projects/', config)
        lengthOfProjects = lengthOfTotalProjects.data.data
    });
</script>

{#if lengthOfProjects.total_projects }
<div class="pt-4">
    <p class="h5">
        Projects
    </p>
    <p class="text-muted">
        {#if lengthOfProjects.total_projects < 2}
            You are {lengthOfProjects.type} of {lengthOfProjects.total_projects} project
        {:else}
            You are {lengthOfProjects.type} of {lengthOfProjects.total_projects} projects
        {/if}
    </p>
</div>
{/if}