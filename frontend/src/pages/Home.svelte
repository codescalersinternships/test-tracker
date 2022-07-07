<script>
    import { onMount } from "svelte";
    import { 
        loadLast5ProjectsUpdated, loadLast5ProjectsActivity
    } from "../healpers/api.js";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Alert from "../components/ui/Alert.svelte";

    export let user;
    let projects, activity, loadData, projectsCopy, thisProject;
    let showDeleteModal = false;


    onMount(async () => {
        loadData = true;
        activity = await loadLast5ProjectsActivity();
        projects = await loadLast5ProjectsUpdated();
        projectsCopy = projects;
        loadData = false;
    });

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        projects = searchProjects;
    };

    function setProject(project) {
        thisProject = project;
        showDeleteModal = true;
    };

    async function handleDelete(event) {
        const project = event.detail.obj;
        const indx = projects.findIndex((v) => v.id === project.id);
        const activityIndx = activity.findIndex((v) => v.project_title === project.title);
        projects = projects;
        activity = activity;
        projects.splice(indx, 1);
        activity.splice(activityIndx, 1);
    }
</script>

<section>
    {#if user}
        <NavBar 
            {user} on:message={
            (event) => {
                if(event.detail.obj.data.type === "project"){
                    projects = projects;
                    projects.unshift(event.detail.obj.data);
                    projects.splice(-1, 1);
                }
            }}
        />
        <div class="container pt-4">
            {#if projects}
                <div class="pt-0">
                    {#if projects && user.permission === "admin"}
                        <p class="h5">
                            <span class="text-primary">
                                Admin
                            </span> 
                            Dashboard
                        </p>
                        <p class="text-muted">
                            There are <strong class="text-primary">{projects.length}</strong>
                            {projects.length === 1 ? "project" : "projects"}
                        </p>
                        {:else if projects && user.permission !== "admin"}
                            <p class="h5">
                                <span class="text-primary">
                                    Member
                                </span> 
                                Dashboard
                            </p>
                            <p class="text-muted">
                                You are <strong class="text-primary">{user.permission}</strong> of <strong>{projects.length}</strong>
                                {projects.length === 1 ? "project" : "projects"}
                            </p>
                        {/if}
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
                    <p class="last-projects">
                        Last <strong class="text-primary">{projects.length}</strong> of
                        {projects.length === 1 ? "Project" : "Projects"} Updated
                    </p>
                    <div class="row p-1">
                        {#each projects as project}
                            <ProjectCard {project}>
                                <button
                                    class="dropdown-item plus-color plus-hover"
                                    on:click={setProject.bind(
                                        undefined,
                                        project
                                    )}>Delete</button
                                >
                            </ProjectCard>
                        {/each}
                    </div>
                    <div class="activity">
                        {#if activity && activity.length > 0}
                            <ActivityTable activity={activity} />
                        {/if}
                    </div>
                </div>
            {:else if loadData}
                <LoodingSpiner />
            {:else}
                <Alert 
                    showAlert = {true} 
                    message = {"There are no projects, try to create one"} 
                    _class = {"info"}
                />
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
</section>

<DeleteModal
    on:message={handleDelete}
    bind:showDeleteModal
    obj={thisProject}
    onRequest="/project"
/>

<svelte:head>
    <title>Test-Tracker | Home</title>
</svelte:head>