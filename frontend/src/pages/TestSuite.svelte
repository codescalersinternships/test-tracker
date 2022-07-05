<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";
    import Alert from "../components/ui/Alert.svelte";

    export let user;
    let testSuites, testSuitesCopy, projectID, thisSuite;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];

        const responseSuites = await axios.get(
            `/test_suites/${projectID}/`,
            config
        );
        testSuites = responseSuites.data.data;
        testSuitesCopy = testSuites;
    });

    async function handleSearch(event) {
        const searchSuites = event.detail.objects;
        testSuites = searchSuites;
    }

    function setSuite(suite) {
        thisSuite = suite;
        showDeleteModal = true;
    }

    async function handleDelete(event) {
        const suite = event.detail.obj;
        const indx = testSuites.findIndex((v) => v.id === suite.id);
        testSuites = testSuites;
        testSuites.splice(indx, 1);
    }
</script>

<svelte:head>
    <title>Test-Tracker | Test Suites</title>
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
        <NavBar projectView="true" 
            {user}
            on:message={
                (event) => {
                    if(event.detail.obj.data.type === "test_suite"){
                        testSuites = testSuites;
                        testSuites.unshift(event.detail.obj.data);
                    }
                }
            }
        />
        <div class="container pt-4 pb-4">
            {#if testSuites}
                <div class="">
                    <strong class="h4">Test Suites</strong>
                    <br />
                    -- There are <strong>{testSuites.length}</strong>
                    Test {testSuites.length === 1 ? "Suite" : "Suites"}
                </div>
                <div class="pt-4">
                    <p>Search Suites</p>
                    <Search
                        request="/test_suites/{projectID}/search/"
                        objects={testSuites}
                        objectsCopy={testSuitesCopy}
                        on:message={handleSearch}
                    />
                </div>
                <div class="pt-5">
                    <p class="search-result" style="display: none">
                        Search Result
                    </p>
                    {#if testSuites && testSuites.length}
                        {#each testSuites as suite}
                            <div class="card mb-3">
                                <Dropdown>
                                    <li>
                                        <button
                                            class="dropdown-item text-danger drop-size plus-hover"
                                            on:click={setSuite(suite)}
                                            >Delete</button
                                        >
                                    </li>
                                </Dropdown>
                                <Link
                                    to="/projects/{projectID}/test-suites/{suite.id}"
                                    class="text-dark d-block text-decoration-none" >
                                    <div class="card-body pb-2">
                                        <h5 class="card-title" style="color: #5a79b1;">
                                            {suite.title}
                                        </h5>
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
                    {:else}
                        <div class="col-12">
                            <Alert 
                                showAlert = {true} 
                                message = {"There are no test suites yet, try to create one"} 
                                _class = {"info"}
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
        obj={thisSuite}
        onRequest="/test_suites/{projectID}/actions"
    />
</section>
