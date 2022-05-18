<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import TotalProjectsLength from "../components/ui/TotalProjectsLength.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Search from "../components/Search.svelte";
    
    export let user;
    let projects, projectsCopy;
    
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const responseProjects = await axios.get('/dashboard/projects/', config);
        projects = responseProjects.data.data;
        projectsCopy = projects= projects;

        for (let project of projects) {
            project.name = project.name.slice(0,25)
        }
    });

    async function searchFunction(){
        const projectName = document.getElementById("search-id").value;
        const config = {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        };

        if(projectName.length > 0){
            const response = await axios.get(
                `/project/search/${projectName}/`,config
            )
            projects = response.data.data
            document.querySelector('.last-projects').style.display = 'none';
            document.querySelector('.search-result').style.display = 'block';
        }else{
            projects = projectsCopy
            document.querySelector('.last-projects').style.display = 'block';
            document.querySelector('.search-result').style.display = 'none';
        }
    }
</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    {#if user}
        <NavBar projectView="true" user={user}/>
        <div class="container">
            <TotalProjectsLength user={user}/>
            <Search title="Search Projects" searchFunction={searchFunction}/>
            
            <div class="pt-5">
                <p class="search-result" style="display: none">Search Result</p>
                <p class="last-projects">All of projects</p>
                <div class="row p-1">
                    {#if projects}
                        {#each projects as project}
                            {#if project.name.length > 25}
                                <ProjectCard title={project.name.slice(0,25)+'..'} date={project.created} link={`/projects/${project.id}`}/>
                            {:else}
                                <ProjectCard title={project.name} date={project.created} link={`/projects/${project.id}`}/>
                            {/if}
                        {:else}
                            <div class="col-12 last-projects-notfound pt-3">
                                <p class="text-muted">
                                    -- There are no projects yet
                                </p>
                            </div>
                        {/each}
                    {:else}
                        <LoodingSpiner />
                    {/if}
                </div>
            </div>            
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
</section>