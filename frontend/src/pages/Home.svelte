<script>
    import { onMount } from 'svelte';
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"


    export let user;
    let projectsCopy, projects, activity, thisProject;
    
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

    async function handleDelete(event) {
        const project = event.detail.obj;
        const indx = projects.findIndex(v => v.id === project.id);
        projects = projects;
        projects.splice(indx, 1);
    }

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        projects = searchProjects;
    }

    function setProject(project) {
        thisProject = project
        document.querySelector('.modal').style.display = 'block'
    }

</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    {#if user}
        <NavBar user={user} />
        <div class="container pt-4">
            {#if projects}
                {#if user.permission !== "admin"}
                    You are <strong>{user.permission}</strong> of 
                    <strong>{user.projects}</strong>
                    {user.projects === 1 ? 'project' : 'projects'}
                {/if}
                <div class="pt-4">
                    <p>
                        Search Projects
                    </p>
                    <Search request="/project/search/" objects={projects} config={config} objectsCopy={projectsCopy} on:message={handleSearch}/>
                </div>
                <div class="pt-5">
                    {#if projects.length > 0}
                        <p class="last-projects">
                            Last <strong>{projects.length}</strong>
                            {projects.length === 1 ? 'Project' : 'Projects'} Updated
                        </p>
                    {/if}
                    <div class="row p-1">
                        {#each projects as project}
                            <ProjectCard project={project} link={`/projects/${project.id}`}>
                                <button class="dropdown-item text-danger" on:click={setProject(project)}>Delete</button>
                            </ProjectCard>
                        {/each}
                    </div>
                </div>
                {#if activity && activity.length > 0}
                    <ActivityTable activity={activity}/>
                {/if}
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
    
    <DeleteModal
        on:message={handleDelete}
        obj={thisProject}
        onRequest='/project'
        config={config}
    />
</section>