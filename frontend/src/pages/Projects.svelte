<script>
    import { onMount } from "svelte";
    import { loadProjects } from "../healpers/api"
    import NavBar from "../components/NavBar.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Alert from "../components/ui/Alert.svelte";

    export let user;

    let projects, projectsCopy, thisProject;
    let showDeleteModal = false;
    let loading = false;

    onMount(async () => {
        loading = true;
        const responseProjects = await loadProjects()
        projects = responseProjects;
        projectsCopy = projects;
        loading = false;
    });

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        projects = searchProjects;
    }

    async function handleDelete(event) {
        const project = event.detail.obj;
        const indx = projects.findIndex((v) => v.id === project.id);
        projects = projects;
        projects.splice(indx, 1);
    }

    function setProject(project) {
        thisProject = project;
        showDeleteModal = true;
    }
</script>

<svelte:head>
    <title>Test-Tracker | Projects</title>
</svelte:head>

<section>
    {#if user}
        <NavBar
            {user} on:message={
            (event) => {
                if(event.detail.obj.data.type === "project"){
                    projects = projects;
                    projects.unshift(event.detail.obj.data);
                }
            }}
        />
        <div class="container pt-4">
            {#if projects}
                <div class="">
                    <strong class="h4 text-primary">All Projects</strong>
                    <br />
                    -- There are <strong class="text-primary">{projects.length}</strong>
                    {projects.length === 1 ? "project" : "projects"}
                </div>
                <div class="pt-4">
                    <p>Search Projects</p>
                    <Search
                        request="/project/search/"
                        objects={projects}
                        objectsCopy={projectsCopy}
                        on:message={handleSearch}
                    />
                </div>
                <div class="pt-5">
                    <div class="row p-1">
                        {#each projects as project}
                            <ProjectCard {project}>
                                <button
                                    class="dropdown-item text-danger drop-size plus-hover"
                                    on:click={setProject(project)}
                                    >Delete</button
                                >
                            </ProjectCard>
                        {/each}
                    </div>
                </div>
            {:else if loading}
                <LoodingSpiner />
            {:else}
                <Alert 
                    showAlert = {true} 
                    message = {"There are no projects, try to create one"} 
                    _class = {"info"}
                />
            {/if}
        </div>
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisProject}
        onRequest="/project"
    />
</section>
