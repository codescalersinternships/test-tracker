<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Search from "../components/Search.svelte";

    export let user;
    let testPlans, testPlansCopy, projectID, planID, planTitle;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };


    onMount(async () => {
        let path = window.location.pathname;
        let lastSlash = path.lastIndexOf('/');
        projectID = path.substring(lastSlash - 1).replace('/test-plans','');

        const responseProjects = await axios.get(`/test_plan/${projectID}/`, config);
        testPlans = responseProjects.data.data;
        testPlansCopy = testPlans;
    });

    async function deletePlan(plan) {
        try {
            await axios.delete(`/test_plan/${projectID}/${planID}/detail/`, config)
            closeModal()
            window.location.reload()
        } catch (err) {
            console.log(err);
        }
    }

    function openModal(plan) {
        planID = plan.id;
        planTitle = plan.title;
        document.querySelector('.modal').style.display = 'block'
    }

    function closeModal() {document.querySelector('.modal').style.display = 'none'}

    async function searchFunction(){
        const projectName = document.getElementById("search-id").value;
        if(projectName.length > 0){
            const response = await axios.get(
                `/project/search/${projectName}/`,config
            )
            projects = response.data.data
            document.querySelector('.last-projects').style.display = 'none';
            document.querySelector('.search-result').style.display = 'block';
        }else{
            projects = projectsCopy
            document.querySelector('.last-projects').style.display = 'block';
            document.querySelector('.search-result').style.display = 'none';
        }
    }
</script>

<svelte:head>
    <title>Test-Tracker | Test Plans</title>
</svelte:head>

<section>
    {#if user && testPlans}
        <NavBar projectView="true" user={user}/>
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5">
                    Test Plans
                </p>
                <p class="text-muted">
                    {#if testPlans.length > 1}
                        There are {testPlans.length} Test Plans
                    {:else}
                        There are {testPlans.length} Test Plan
                    {/if}
                </p>
            </div>
            <Search title="Search On Plan" searchFunction={searchFunction}/>
            <div class="pt-5">
                <p class="search-result" style="display: none">Search Result</p>
                {#each testPlans as plan}
                    <div class="card mb-3" style="padding: 20px;">
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
                                        <a href="/projects/{projectID}/test-plans/{plan.id}"
                                            class="dropdown-item text-black">View</a>
                                    </li>
                                    <li>
                                        <button class="dropdown-item text-danger" on:click={openModal(plan)}>Delete</button>
                                    </li>
                                </ul>
                            </div>
                            <h5 class="card-title">{plan.title}</h5>
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
                    <small>Please note that after delete <strong>{planTitle}</strong> you will lose all of sub plans</small>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={closeModal}>Close</button>
                    <button type="button" class="btn btn-danger text-white text-decoration-none" on:click={deletePlan(planID)}>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
