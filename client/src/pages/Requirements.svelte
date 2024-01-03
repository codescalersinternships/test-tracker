<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";
    import Alert from "../components/ui/Alert.svelte";

    export let user;
    let requirements, requirementsCopy, projectID, thisRequirement;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        try {
            const responseReq = await axios.get(
                `/requirements/projects/${projectID}/get-all/`,
                config
            );
            requirements = responseReq.data.results;
            requirementsCopy = requirements;
        } catch (error) {
            if (error.response.status == 403 || error.response.status == 404) {
                window.location.href = "/not-found";
            }
        }
    });

    function setRequirement(requirement) {
        thisRequirement = requirement;
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
    {#if user && requirements}
        <NavBar 
            projectView="true"
            {user} 
            on:message={
                (event) => {
                    if(event.detail.obj.data.type === "requirement_Doc"){
                        requirements = requirements;
                        requirements.unshift(event.detail.obj.data);
                    }
                }
            }
        />
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5 text-primary">Project Requirements Docs</p>
                <p class="text-muted">
                    There are <strong class="text-primary">{requirements.length}</strong>
                    Test {requirements.length === 1
                        ? "Requirement"
                        : "Requirements"}
                </p>
            </div>
            <div class="pt-4">
                <p>Search Requirements Docs</p>
                <Search
                    request="/requirements/projects/{projectID}/search/"
                    objects={requirements}
                    objectsCopy={requirementsCopy}
                    on:message={handleSearch}
                />
            </div>
            <div class="pt-5">
                <p class="search-result" style="display: none">Search Result</p>
                {#if requirements && requirements.length}
                    {#each requirements as requirement}
                        <div class="card mb-3">
                            <Dropdown>
                                <li>
                                    <button
                                        class="dropdown-item text-danger drop-size plus-hover"
                                        on:click={setRequirement(requirement)}
                                        >Delete</button
                                    >
                                </li>
                            </Dropdown>
                            <Link to="/projects/{projectID}/requirements/{requirement.id}"
                                class="text-dark d-block text-decoration-none">
                                <div class="card-body pb-2">
                                    <h5 class="card-title text-primary">
                                        {requirement.title}
                                    </h5>
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
                                            <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                                <p class="text-muted">
                                                    Number of requirements:
                                                    <strong>{requirement.requirements.length}</strong>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    {/each}
                {:else}
                    <Alert 
                        showAlert = {true} 
                        message = {"There are no project requirement docs, try to create one"} 
                        _class = {"info"}
                    />
                {/if}
            </div>
        </div>
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisRequirement}
        onRequest="/requirements/projects/{projectID}/details"
    />
</section>

<svelte:head>
    <title>Test-Tracker | Requirements</title>
    <style>
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            width: 35px; 
            top:20px
        }
    </style>
</svelte:head>