<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'

    import NavBar from "../components/NavBar.svelte";
    import Projects from "../components/Projects.svelte";
    import Search from "../components/Search.svelte";

    let lengthOfProjects = {}

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const response = await axios.get('/dashboard/total_projects/', config)
        lengthOfProjects = response.data.data
        return lengthOfProjects
    });
</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    <NavBar projectView="true"/>
    <div class="container">
        {#if lengthOfProjects.total_projects }
            <div class="pt-4">
                <p class="text-muted">
                    {#if lengthOfProjects.total_projects < 2}
                        You are {lengthOfProjects.type} of {lengthOfProjects.total_projects} project
                    {:else}
                        You are {lengthOfProjects.type} of {lengthOfProjects.total_projects} projects
                    {/if}
                </p>
            </div>
        {/if}
        <Search />
        <Projects />
    </div>
</section>