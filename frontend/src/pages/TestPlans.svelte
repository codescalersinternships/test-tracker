<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";

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
</script>

<svelte:head>
    <title>Test-Tracker | Test Plans</title>
</svelte:head>

<section>
    {#if user}
        <NavBar projectView="true" {user} />
        <div class="container pt-4 pb-4">
            {#if testPlans}
                <div class="">
                    <strong class="h4">Test Plans</strong>
                    <br />
                    -- There are <strong>{testPlans.length}</strong>
                    Test {testPlans.length === 1 ? "Plan" : "Plans"}
                </div>
                <div class="pt-4">
                    <p>Search Plans</p>
                    <Search
                        request="/test_plan/{projectID}/search/"
                        objects={testPlans}
                        {config}
                        objectsCopy={testPlansCopy}
                        on:message={handleSearch}
                    />
                </div>
                <div class="pt-5">
                    <p class="search-result" style="display: none">
                        Search Result
                    </p>
                    {#each testPlans as plan}
                        <div class="card mb-3" style="background: #f9f9f9;">
                            <div
                                class="dropdown p-1"
                                style="position: absolute;font-size: 0;right: 0;width: 35px; top:20px"
                            >
                                <a
                                    class="dropdown-toggle"
                                    id="dropdownMenuButton"
                                    data-mdb-toggle="dropdown"
                                    aria-expanded="false"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="20"
                                        height="20"
                                        fill="currentColor"
                                        class="bi bi-three-dots-vertical"
                                        viewBox="0 0 16 16"
                                    >
                                        <path
                                            d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"
                                        />
                                    </svg>
                                </a>
                                <ul
                                    class="dropdown-menu"
                                    aria-labelledby="dropdownMenuButton"
                                >
                                    <li>
                                        <button
                                            class="dropdown-item text-danger"
                                            on:click={setPlan(plan)}
                                            >Delete</button
                                        >
                                    </li>
                                </ul>
                            </div>
                            <Link
                                to="/projects/{projectID}/test-plans/{plan.id}"
                                class="text-dark d-block text-decoration-none"
                            >
                                <div class="card-body pb-2">
                                    <h5
                                        class="card-title"
                                        style="color: #5a79b1;"
                                    >
                                        {plan.title}
                                    </h5>
                                    <div class="pt-4">
                                        <div class="row">
                                            <div
                                                class="col-6 col-md-6 col-sm-6 col-xs-8"
                                            >
                                                <p class="text-muted">
                                                    Created: <strong
                                                        >{plan.created}</strong
                                                    >
                                                </p>
                                            </div>
                                            <div
                                                class="col-6 col-md-6 col-sm-6 col-xs-8"
                                            >
                                                <p class="text-muted">
                                                    Updated: <strong
                                                        >{plan.modified}</strong
                                                    >
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="col-12 pt-5">
                    <p class="text-muted">-- There are no plans yet</p>
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
        {config}
    />
</section>
