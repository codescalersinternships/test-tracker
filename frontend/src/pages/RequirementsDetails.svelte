<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    let projectRequirement, thisReq, requirements, requirementsCopy, errorMessage;
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let projectReqID = path.split("/")[4];
    
    onMount(async () => {
        // Loading Project RequirementsDetails
        try {
            const responseReq = await axios.get(`requirements/projects/${projectID}/details/${projectReqID}/`, config);
            projectRequirement = responseReq.data.data;
            requirements = projectRequirement.requirements
            requirementsCopy = requirements
        } catch (error) {
            if (error.response.status == 403 || error.response.status == 404) {
                window.location.href = '/not-found/'
            }
        }
    });

    async function deleteRequirement(thisReq){
        try {
            const indx = projectRequirement.requirements.findIndex(v => v.id === thisReq.id);
            closeModal(thisReq, 'delete')
            await axios.delete(
                `requirements/projects/${projectID}/${projectReqID}/${thisReq.id}/`, config
            );
            requirements = requirements;
            requirements.splice(indx, 1);
        } catch (error) {
            console.log(error);
        }
    }

    async function updateRequirement(thisReq){
        // Update requirement function
        let data = {title:thisReq.title, description:thisReq.description}
        try {
            const indx = projectRequirement.requirements.findIndex(v => v.id === thisReq.id);
            closeModal(thisReq, 'update')
            const response = await axios.put(
                `requirements/projects/${projectID}/${projectReqID}/${thisReq.id}/`, data, config
            );
            requirements = requirements;

            requirements[indx] = response.data.data
        } catch (error) {
            console.log(error);
        }
    }

    async function searchRequirements(){
        // Search on test plan contents
        const title = document.getElementById("search-id").value;
        if(title.length > 0){
            const response = await axios.get(
                `requirements/projects/${projectID}/search/requirements/${title}/`,config
            )
            requirements = response.data.data
        }else{
            requirements = requirementsCopy
        }
    }

    function setREQ(requirement, event) {
        // Just set the title and body global to get the current values and display the modal;
        thisReq = requirement;
        if(event === "delete"){
            document.querySelector('.delete-requirement').style.display = 'block'
        } else{
            document.querySelector('.update-requirement').style.display = 'block'
        }
    }

    function closeModal(requirement, event) {
        // Close the modal based on event
        if(event === "delete"){
            document.querySelector('.delete-requirement').style.display = 'none'
        } else{
            document.querySelector('.update-requirement').style.display = 'none'
        }
    }

</script>

<svelte:head>
    <title>Test-Tracker | Requirements Detail</title>
</svelte:head>


<section>
    {#if user && projectRequirement}
        <NavBar projectView="true" user={user}/>
        <Alert message={errorMessage}/>

        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5">
                    {projectRequirement.title}
                </p>
                <p class="text-muted">
                    {#if projectRequirement.requirements.length}
                        There are <strong>{projectRequirement.requirements.length}</strong> 
                        {projectRequirement.requirements.length === 1 ? 'Requirement' : 'Requirements'}
                    {/if}
                </p>
            </div>
            <div class="row mt-4">
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Created : {projectRequirement.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Updated : {projectRequirement.updated}</p>
                        </div>
                    </div>
                </div>
            </div>
            <Search title="Search On Contents" searchFunction={searchRequirements}/>
            <div class="pt-5">
                {#if requirements.length > 0}
                    {#each requirements as requirement }
                        <div class="card mb-3">
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
                                            <button on:click={setREQ(requirement, "update")} 
                                                class="dropdown-item text-black">Update</button>
                                        </li>
                                        <li>
                                            <button class="dropdown-item text-danger" on:click={setREQ(requirement, "delete")}>Delete</button>
                                        </li>
                                    </ul>
                                </div>
                                <h5 class="card-title">{requirement.title}</h5>
                                <p class="mt-4 text-muted">{requirement.description}</p>
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
    <!-- Modal -->
    
        <div class="modal delete-requirement" tabindex="-1" style="display: none;">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body p-4">
                        <div class="modal-header">
                            <h5>Confirmation Required</h5>
                        </div>
                        {#if thisReq}
                        <strong class="text-muted pt-3 mb-3">
                            You are about to delete 
                            <small class="text-bold">
                                {thisReq.title}.
                            </small>
                        </strong>
                        {/if}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={closeModal(thisReq,"delete")}>Close</button>
                        <button type="button" class="btn btn-danger text-white text-decoration-none" on:click={deleteRequirement(thisReq)}>
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal update-requirement" tabindex="-1" style="display: none;">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body p-4">
                        <div class="modal-header">
                            <h5>Update requirement</h5>
                        </div>
                        <form>
                            {#if thisReq}
                                <div class="form-group p-2">
                                    <label for="content-title">Title</label>
                                    <input bind:value="{thisReq.title}" type="text" class="form-control" id="content-title">
                                </div>
                                <div class="form-group p-2">
                                    <label for="content-body">Description</label>
                                    <textarea bind:value="{thisReq.description}" class="form-control" id="content-body"></textarea>
                                </div>
                            {/if}
                        </form>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" 
                                on:click={closeModal(thisReq,"update")}>Close</button>
                            <button class="btn btn-success" data-mdb-dismiss="modal" 
                                on:click={updateRequirement(thisReq)}>Update</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</section>


<style>
    textarea {
        height: 150px; 
        max-height: 150px
    }
</style>
