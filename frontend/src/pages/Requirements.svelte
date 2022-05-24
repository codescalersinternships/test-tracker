<script>
    import { onMount } from 'svelte';
    import { Link } from "svelte-navigator";
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"

    export let user;
    let requirements, requirementsCopy, projectID, thisRequirement

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };


    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        try {
            const responseReq = await axios.get(`/requirements/projects/${projectID}/get-all/`, config);
            requirements = responseReq.data.data;
            requirementsCopy = requirements;
        } catch (error) {
            if (error.response.status == 403 || error.response.status == 404) {
                window.location.href = '/not-found'
            }
        }
    });

    function setRequirement(requirement) {
        thisRequirement = requirement
        document.querySelector('.modal').style.display = 'block'
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

<svelte:head>
    <title>Test-Tracker | Requirements</title>
</svelte:head>

<section>
    {#if user && requirements}
        <NavBar projectView="true" user={user}/>
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5">
                    Project Requirements Docs
                </p>
                <p class="text-muted">
                    There are <strong>{requirements.length}</strong> 
                    Test {requirements.length === 1 ? 'Requirement' : 'Requirements'}
                </p>
            </div>
            <div class="pt-4">
                <p>
                    Search Requirements Docs
                </p>
                <Search request="/requirements/projects/{projectID}/search/" objects={requirements} config={config} 
                    objectsCopy={requirementsCopy} on:message={handleSearch}/>
            </div>
            <div class="pt-5">
                <p class="search-result" style="display: none">Search Result</p>
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
                        <Link to="/projects/{projectID}/requirements/{requirement.id}" class="text-dark d-block text-decoration-none">
                            <div class="card-body pb-2">
                                <h5 class="card-title" style="color: #5a79b1;">{requirement.title}</h5>
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
                                                Number of requirements: <strong>{requirement.requirements.length}</strong>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    </div>
                {/each}
            </div>   
        </div>
    {/if}
    <DeleteModal
        on:message={handleDelete}
        obj={thisRequirement}
        onRequest='/requirements/projects/{projectID}/details'
        config={config}
    />
</section>
