<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"
    
    export let user;

    let projects, projectsCopy, thisProject;
    
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const responseProjects = await axios.get('/dashboard/projects/', config);
        projects = responseProjects.data.data;
        projectsCopy = projects;
    });

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        projects = searchProjects;
    }

    async function handleDelete(event) {
        const project = event.detail.obj;
        const indx = projects.findIndex(v => v.id === project.id);
        projects = projects;
        projects.splice(indx, 1);
    }

    function setProject(project) {
        thisProject = project
        document.querySelector('.modal').style.display = 'block'
    }

</script>

<svelte:head>
    <title>Test-Tracker | Projects</title>
</svelte:head>

<section>
    {#if user}
        <NavBar user={user}/>
        <div class="container pt-4">
            {#if projects}
                There are <strong>{projects.length}</strong> 
                {projects.length === 1 ? 'project' : 'projects'}
                <div class="pt-4">
                    <p>
                        Search Projects
                    </p>
                    <Search request="/project/search/" objects={projects} config={config} objectsCopy={projectsCopy} on:message={handleSearch}/>
                </div>
                <div class="pt-5">
                    <div class="row p-1">
                        {#each projects as project}
                            <ProjectCard project={project} link={`/projects/${project.id}`}>
                                <button class="dropdown-item text-danger" on:click={setProject(project)}>Delete</button>
                            </ProjectCard>
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
    <DeleteModal
        on:message={handleDelete}
        obj={thisProject}
        onRequest='/project'
        config={config}
    />
</section>