<script>
    import { onMount } from 'svelte';
    import { Link } from "svelte-navigator";

    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";

    export let user;
    let testSuites, testSuitesCopy, projectID, thisSuite;
    let show = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };


    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];

        const responseSuites = await axios.get(`/test_suites/${projectID}/`, config);
        testSuites = responseSuites.data.data;
        testSuitesCopy = testSuites;
    });

    async function handleSearch(event) {
        const searchSuites = event.detail.objects;
        testSuites = searchSuites;
    }

    function setSuite(suite) {
        thisSuite = suite;
        show = true;
    }

    async function handleDelete(event) {
        const suite = event.detail.obj;
        const indx = testSuites.findIndex(v => v.id === suite.id);
        testSuites = testSuites;
        testSuites.splice(indx, 1);
    }

</script>

<svelte:head>
    <title>Test-Tracker | Test Suites</title>
</svelte:head>

<section>
    {#if user}
        <NavBar projectView="true" user={user}/>
        <div class="container pt-4 pb-4">
            {#if testSuites}
                <div class="">
                    <strong class="h4">Test Suites</strong>
                    <br>
                    -- There are <strong>{testSuites.length}</strong> 
                        Test {testSuites.length === 1 ? 'Suite' : 'Suites'}
                </div>
                <div class="pt-4">
                    <p>
                        Search Suites
                    </p>
                    <Search request="/test_suites/{projectID}/search/" objects={testSuites} config={config} 
                        objectsCopy={testSuitesCopy} on:message={handleSearch}/>
                </div>
                <div class="pt-5">
                    <p class="search-result" style="display: none">Search Result</p>
                    {#each testSuites as suite}
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
                                        <button class="dropdown-item text-danger" on:click={setSuite(suite)}>Delete</button>
                                    </li>
                                </ul>
                            </div>
                            <Link to="/projects/{projectID}/test-suites/{suite.id}" class="text-dark d-block text-decoration-none">
                                <div class="card-body pb-2">
                                    <h5 class="card-title" style="color: #5a79b1;">{suite.title}</h5>
                                    <div class="pt-4">
                                        <div class="row">
                                            <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                                <p class="text-muted">
                                                    Created: <strong>{suite.created}</strong>
                                                </p>
                                            </div>
                                            <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                                <p class="text-muted">
                                                    Updated: <strong>{suite.modified}</strong>
                                                </p>
                                            </div>
                                            <div class="col-12 col-md-4 col-sm-6 col-xs-8">
                                                <p class="text-muted">
                                                    Number of test cases: <strong>{suite.number_of_test_cases}</strong>
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
                    <p class="text-muted">
                        -- There are no test suites yet
                    </p>
                </div>
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
    <DeleteModal
        bind:show
        on:message={handleDelete}
        obj={thisSuite}
        onRequest='/test_suites/{projectID}/actions'
        config={config}
    />
</section>
