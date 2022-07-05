<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let RequirementDocs, thisReq, requirements, requirementsCopy;
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let projectReqID = path.split("/")[4];
    let showDeleteModal = false;

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
        showDeleteModal = true;
    }

    async function handleDelete(event) {
        const requirement = event.detail.obj;
        const indx = requirements.findIndex((v) => v.id === requirement.id);
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
        <NavBar projectView="true" 
            {user}
            on:message={
                (event) => {
                    if(event.detail.obj.data.type === "requirement"){
                        requirements = requirements;
                        requirements.unshift(event.detail.obj.data);
                    }
                }
            }
        />
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
                <p>Search Requirements</p>
                <Search
                    request="/requirements/projects/{projectID}/search/requirements/"
                    objects={requirements}
                    objectsCopy={requirementsCopy}
                    on:message={handleSearch}
                />
            </div>
            <div class="pt-5">
                {#if requirements.length > 0}
                    {#each requirements as requirement}
                        <div class="card mb-3">
                            <Dropdown>
                                <li>
                                    <button
                                        class="dropdown-item text-danger drop-size plus-hover"
                                        on:click={setRequirement(
                                            requirement
                                        )}
                                        >Delete
                                    </button>
                                </li>
                            </Dropdown>
                            <div class="card-body pb-2">
                                <span class="text-primary h5">
                                    {requirement.requirement_title}
                                </span>
                                <span class="text-muted h5">
                                    {requirement.title}
                                </span>
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
                    <Alert 
                        showAlert = {true} 
                        message = {"There are no requirements fot this document, try to adding one."} 
                        _class = {"info"}
                    />
                {/if}
            </div>
        </div>
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisReq}
        onRequest="/requirements/projects/{projectID}/{projectReqID}"
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
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            width: 35px; 
            top:20px
        }
    </style>
</svelte:head>
