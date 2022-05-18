<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'

    import NavBar from "../components/NavBar.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";

    let lengthOfProjects = {}
    let projects = []
    
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const lengthOfTotalProjects = await axios.get('/dashboard/total_projects/', config)
        const last5Projects = await axios.get('/project/last-5-projects/', config)
        lengthOfProjects = lengthOfTotalProjects.data.data
        projects = last5Projects.data.data
    });
</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    <NavBar />
    <div class="container">
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
        <Search />
        <div class="pt-5 last-projects">
            <p>Latest Projects</p>
            <div class="row p-1">
                {#each projects as project}
                    {#if project.name.length > 25}
                        <ProjectCard title={project.name.slice(0,25)+'..'} date={project.created} link={`/projects/${project.id}`}/>
                    {:else}
                        <ProjectCard title={project.name} date={project.created} link={`/projects/${project.id}`}/>
                    {/if}
                {:else}
                    <div class="col-12">
                        <p class="text-muted">
                            -- There are no projects yet
                        </p>
                    </div>
                {/each}
            </div>
        </div>
        <ActivityTable endPoint='/project/last-5-projects/activity/'/>
    </div>
</section>