<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let RequirementDocs, thisReq, requirements, requirementsCopy, errorMessage;
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let projectReqID = path.split("/")[4];
    let show = false;

    onMount(async () => {
        // Loading Project RequirementsDetails
        try {
            const responseReq = await axios.get(
                `requirements/projects/${projectID}/details/${projectReqID}/`,
                config
            );
            RequirementDocs = responseReq.data.data;
            requirements = RequirementDocs.requirements;
            requirementsCopy = requirements;
        } catch (error) {
            if (error.response.status == 403 || error.response.status == 404) {
                window.location.href = "/not-found/";
            }
        }
    });

    function setRequirement(requirement) {
        thisReq = requirement;
        show = true;
    }

    async function handleDelete(event) {
        const requirement = event.detail.obj;
        const indx = requirements.findIndex(v => v.id === requirement.id);
        requirements = requirements;
        requirements.splice(indx, 1);
    }

    async function handleSearch(event) {
        const searchRequirements = event.detail.objects;
        requirements = searchRequirements;
    }
</script>

<section>
    {#if user && RequirementDocs}
        <NavBar projectView="true" {user} />
        <Alert message={errorMessage} />

        <div class="container pb-5">
            <div class="pt-4">
                <p class="h4 mb-2">
                    Requirement Docs | 
                    <strong class="h4 title">{RequirementDocs.title}</strong>
                </p>

                <p class="text-muted">
                    {#if RequirementDocs.requirements.length}
                        There are <strong
                            >{RequirementDocs.requirements.length}</strong
                        >
                        {RequirementDocs.requirements.length === 1
                            ? "Requirement"
                            : "Requirements"}
                    {/if}
                </p>
            </div>
            <div class="row mt-4">
                <div class="col-6">
                    <div
                        class="card mb-3 text-center"
                        style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Created : {RequirementDocs.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div
                        class="card mb-3 text-center"
                        style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Updated : {RequirementDocs.updated}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="pt-4">
                <p>
                    Search Requirements
                </p>
                <Search request="/requirements/projects/{projectID}/search/requirements/" 
                    objects={requirements} config={config} 
                    objectsCopy={requirementsCopy} on:message={handleSearch}/>
            </div>
            <div class="pt-5">
                {#if requirements.length > 0}
                    {#each requirements as requirement}
                        <div class="card mb-3" style="background: #f9f9f9;">
                            <div class="dropdown p-1" style="position: absolute;font-size: 0;right: 0;width: 35px; top:20px">
                                <a
                                    class="dropdown-toggle"
                                    id="dropdownMenuButton"
                                    data-mdb-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" 
                                    class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                    <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                </svg>
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                    <li>
                                        <button class="dropdown-item text-danger" on:click={setRequirement(requirement)}>Delete</button>
                                    </li>
                                </ul>
                            </div>
                            <div class="card-body pb-2">
                                <h5 class="card-title" style="color: #5a79b1;">{requirement.requirement_title}-{requirement.title}</h5>
                                <p class="mt-4 text-muted">
                                    {requirement.description}
                                </p>
                                <div class="pt-4">
                                    <div class="row">
                                        <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                            <p class="text-muted">
                                                Created: <strong>{requirement.created}</strong>
                                            </p>
                                        </div>
                                        <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                            <p class="text-muted">
                                                Updated: <strong>{requirement.updated}</strong>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/each}
                {:else}
                    <div class="col-12 last-projects-notfound pt-3">
                        <p class="text-muted">
                            -- There are no requirements fot this requirement
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
    <DeleteModal
        bind:show
        on:message={handleDelete}
        obj={thisReq}
        onRequest='/requirements/projects/{projectID}/{projectReqID}'
        config={config}
    />
</section>

<svelte:head>
    <title>Test-Tracker | Requirements Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
    </style>
</svelte:head>