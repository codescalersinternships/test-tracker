<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    
    export let user;

    let projects, projectsCopy, host;
    
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const responseProjects = await axios.get('/dashboard/projects/', config);
        projects = responseProjects.data.data;
        projectsCopy = projects;

        for (let project of projects) {
            host = project.user
            project.name = project.name.slice(0,25)
        }
    });

    async function searchFunction(){
        const projectName = document.getElementById("search-id").value;
        if ( projectName.length > 0){
            const response = await axios.get(
                `/project/search/${projectName}/`,config
            )
            projects = response.data.data
        }else{
            console.log("Yes");
            projects = projectsCopy
        }
    }
</script>

<svelte:head>
    <title>Test-Tracker | Projects</title>
</svelte:head>

<section>
    {#if user}
        <NavBar user={user}/>
        <div class="container pt-4">
            {#if projects && host}
                There are <strong>{projects.length}</strong> 
                of {projects.length === 1 ? 'project' : 'projects'} created by <strong>{host}</strong>
                <Search title="Search Projects" searchFunction={searchFunction}/>
                <div class="pt-5">
                    <div class="row p-1">
                        {#each projects as project}
                            <ProjectCard title={project.name.length > 25 ? project.name.slice(0,25)+'..' : project.name} 
                                date={project.created} link={`/projects/${project.id}`}/>
                        {/each}
                    </div>
                </div>
            {:else}
                <div class="col-12 last-projects-notfound pt-3">
                    <p class="text-muted">
                        -- There are no projects yet
                    </p>
                </div>
            {/if}
        </div>
    {/if}
</section>