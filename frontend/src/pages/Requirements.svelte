<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";

    export let user;
    let requirements, requirementsCopy, projectID, requirementTitle, requirementID

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
            if (error.response.status == 404) {
                window.location.href = '/not-found'
            }
        }
    });

    async function deleteRequirement(requirement) {
        try {
            const indx = requirements.findIndex(v => v.id === requirement);
            await axios.delete(`/requirements/projects/${projectID}/update/${requirementID}/`, config)
            closeModal()
            requirements = requirements;
            requirements.splice(indx, 1);
        } catch (err) {
            console.log(err);
        }
    }

    function openModal(requirement) {
        requirementID = requirement.id;
        requirementTitle = requirement.title;
        document.querySelector('.modal').style.display = 'block'
    }

    function closeModal() {document.querySelector('.modal').style.display = 'none'}

    async function searchFunction(){
        const word = document.getElementById("search-id").value;
        if(word.length > 0){
            const response = await axios.get(
                `/requirements/projects/${projectID}/search/${word}/`,config
            )
            requirements = response.data.data

        }else{
            requirements = requirementsCopy
        }
    }

</script>

<svelte:head>
    <title>Test-Tracker | Test Plans</title>
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
            <Search title="Search On Plan" searchFunction={searchFunction}/>
            <div class="pt-5">
                <p class="search-result" style="display: none">Search Result</p>
                {#each requirements as requirement}
                    <div class="card mb-3" style="padding: 20px; background: #f9f9f9;">
                        <div class="card-body pb-2">
                            <div class="dropdown p-1" style="position: absolute;font-size: 0;right: 0;width: 35px;">
                                <a
                                    class="dropdown-toggle"
                                    id="dropdownMenuButton"
                                    data-mdb-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                    <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                </svg>
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                    <li>
                                        <a href="/projects/{projectID}/requirements/{requirement.id}"
                                            class="dropdown-item text-black">View</a>
                                    </li>
                                    <li>
                                        <button class="dropdown-item text-danger" on:click={openModal(requirement)}>Delete</button>
                                    </li>
                                </ul>
                            </div>
                            <h5 class="card-title">{requirement.title}</h5>
                            <div class="pt-4">
                                <div class="row">
                                    <div class="col-4 col-md-4 col-sm-6 col-xs-8">
                                        <p class="text-muted">
                                            Created: <strong>{requirement.created}</strong>
                                        </p>
                                    </div>
                                    <div class="col-4 col-md-4 col-sm-6 col-xs-8">
                                        <p class="text-muted">
                                            Updated: <strong>{requirement.updated}</strong>
                                        </p>
                                    </div>
                                    <div class="col-4 col-md-4 col-sm-6 col-xs-8">
                                        <p class="text-muted">
                                            Requirements: <strong>{requirement.requirements.length}</strong>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>   
        </div>
    {/if}

    <!-- Modal -->
    <div class="modal" tabindex="-1" style="display: none;">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">You are about to delete this plan.</h5>
                </div>
                <div class="modal-body">
                    <small>Please note that after delete <strong>{requirementTitle}</strong> you will lose all of sub requirements</small>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={closeModal}>Close</button>
                    <button type="button" class="btn btn-danger text-white text-decoration-none" on:click={deleteRequirement(requirementID)}>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
