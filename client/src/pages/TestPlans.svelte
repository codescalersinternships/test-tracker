<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";

    export let user;
    let testPlans, testPlansCopy, projectID, thisTestPlan;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];

        const responsePlans = await axios.get(
            `/test_plan/${projectID}/`,
            config
        );
        testPlans = responsePlans.data.data;
        testPlansCopy = testPlans;
    });

    async function handleSearch(event) {
        const searchPlans = event.detail.objects;
        testPlans = searchPlans;
    }

    function setPlan(plan) {
        thisTestPlan = plan;
        showDeleteModal = true;
    }

    async function handleDelete(event) {
        const plan = event.detail.obj;
        const indx = testPlans.findIndex((v) => v.id === plan.id);
        testPlans = testPlans;
        testPlans.splice(indx, 1);
    }

    async function handlePostNewObject(event) {
        const plan = event.detail.obj;
        testPlans = testPlans;
        testPlans.unshift(plan.data);
    }
</script>

<svelte:head>
    <title>Test-Tracker | Test Plans</title>
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

<section>
    {#if user}
        <NavBar 
            projectView="true" 
            {user} on:message={
            (event) => {
                if(event.detail.obj.data.type === "test_plan"){
                    testPlans = testPlans;
                    testPlans.unshift(event.detail.obj.data);
                }
            }}
        />
        <div class="container pt-4 pb-4">
            {#if testPlans}
                <div class="">
                    <strong class="h4 text-primary">Test Plans</strong>
                    <br />
                    -- There are <strong class="text-primary">{testPlans.length}</strong>
                    Test {testPlans.length === 1 ? "Plan" : "Plans"}
                </div>
                <div class="pt-4">
                    <p>Search Plans</p>
                    <Search
                        request="/test_plan/{projectID}/search/"
                        objects={testPlans}
                        objectsCopy={testPlansCopy}
                        on:message={handleSearch}
                    />
                </div>
                <div class="pt-5">
                    <p class="search-result" style="display: none">
                        Search Result
                    </p>
                    {#if testPlans && testPlans.length > 0}
                        {#each testPlans as plan}
                            <div class="card mb-3">
                                <Dropdown>
                                    <li>
                                        <button
                                            class="dropdown-item text-danger drop-size plus-hover"
                                            on:click={setPlan(plan)}
                                            >Delete</button
                                        >
                                    </li>
                                </Dropdown>
                                <Link to="/projects/{projectID}/test-plans/{plan.id}"
                                    class="text-primary d-block text-decoration-none">
                                    <div class="card-body pb-2">
                                        <h5 class="card-title text-primary">
                                            {plan.title}
                                        </h5>
                                        <div class="pt-4">
                                            <div class="row">
                                                <div class="col-6 col-md-6 col-sm-6 col-xs-8">
                                                    <p class="text-muted">
                                                        Created: <strong>{plan.created}</strong>
                                                    </p>
                                                </div>
                                                <div class="col-6 col-md-6 col-sm-6 col-xs-8">
                                                    <p class="text-muted">
                                                        Updated: <strong>{plan.modified}</strong>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </Link>
                            </div>
                        {/each}
                    {:else}
                        <div class="col-12">
                            <Alert 
                                _class={'info'} 
                                showAlert={true} 
                                message={"There are no plans yet, Try to add new plan."} 
                            />
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisTestPlan}
        onRequest="/test_plan/{projectID}/actions"
    />
</section>
