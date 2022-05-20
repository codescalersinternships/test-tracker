<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";


    export let user;
    let projectsCopy, projects, activity;
    
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const responseProjects = await axios.get('/project/last-5-projects/', config);
        const responseActivity = await axios.get('/project/last-5-projects/activity/', config)
        activity = responseActivity.data.data
        projects = await responseProjects.data.data;
        projectsCopy = projects;
    });

    async function searchFunction(){
        const projectName = document.getElementById("search-id").value;
        if(projectName.length > 0){
            const response = await axios.get(
                `/project/search/${projectName}/`,config
            )
            projects = response.data.data
        }else{
            projects = projectsCopy
        }
    }

</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    {#if user && projects}
        <NavBar user={user} />
        <div class="container pt-4">
            You are <strong>{user.permission}</strong> of 
            <strong>{user.projects}</strong>
            {user.projects === 1 ? 'project' : 'projects'}

            <Search title="Search Projects" searchFunction={searchFunction}/>
            <div class="pt-5">
                <p class="last-projects">Last <strong>{user.projects}</strong>
                    {user.projects === 1 ? 'Project' : 'Projects'} Updated</p>
                <div class="row p-1">
                    {#each projects as project}
                        <ProjectCard title={project.name.length > 25 ? project.name.slice(0,25)+'..' : project.name} 
                            date={project.created} link={`/projects/${project.id}`}/>
                    {:else}
                        <div class="col-12 last-projects-notfound pt-3">
                            <p class="text-muted">
                                -- There are no projects yet
                            </p>
                        </div>
                    {/each}
                </div>
            </div>   
            <ActivityTable activity={activity}/>
        </div>
    {/if}
</section>