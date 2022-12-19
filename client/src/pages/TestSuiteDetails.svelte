<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import AddNewSection from "../components/Sections/AddNewSection.svelte";
    import TestSuiteSections from "../components/Sections/TestSuiteSections.svelte";

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let testSuite, testSuiteCopy, projectID, suiteID, thisTestCase;
    let showDeleteModal = false;

    onMount(async () => {
        // Loading test suite
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        suiteID = path.split("/")[4];
        try {
            const responseSuites = await axios.get(
                `test_suites/${projectID}/actions/${suiteID}/`,
                config
            );
            testSuite = responseSuites.data.data;
            testSuiteCopy = testSuite;
        } catch (error) {
            if (error.response.status == 404) {
                window.location.href = "/not-found/";
            }
        }
    });

    async function handleSearch(event) {
        const searchTestCase = event.detail.objects;
        testSuite.test_cases = searchTestCase;
    }

    async function handleDelete(event) {
        const testCase = event.detail.obj;
        const indx = testSuite.test_cases.findIndex(
            (v) => v.id === testCase.id
        );
        testSuite = testSuite;
        testSuite.test_cases.splice(indx, 1);
    }
</script>

{#if user}
    <NavBar projectView="true" 
        {user}
        on:message={
            (event) => {
                if(event.detail.obj.data.type === "test_case"){
                    testSuite.test_cases = testSuite.test_cases;
                    testSuite.test_cases.unshift(event.detail.obj.data);
                }
            }
        }
    />
    {#if testSuite}
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h4 mb-2">
                    Test Suite |
                    <strong class="h4 text-primary">{testSuite.title}</strong>
                </p>
                <p class="text-muted">
                    There are <strong class="text-primary">{testSuite.number_of_test_cases}</strong>
                    test {testSuite.number_of_test_cases === 1
                        ? "case"
                        : "cses"}
                </p>
            </div>
            <div class="row mb-4">
                <div class="col-6">
                    <div
                        class="card mb-3 text-center btn-primary"
                        style="font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Created : {testSuite.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div
                        class="card mb-3 text-center btn-primary"
                        style="font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Updated : {testSuite.modified}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card_info card">
                        <p>Associated test plan</p>
                        {#if testSuite.test_plan}
                            <a
                                href="/projects/{projectID}/test-plans/{testSuite
                                    .test_plan.id}"
                                class="text-decoration-none text-primary"
                            >
                                <div class="card-body p-0 text-center">
                                    {testSuite.test_plan.title}
                                </div>
                            </a>
                        {:else}
                            <p class="text-muted">No associated plan</p>
                        {/if}
                    </div>
                </div>
            </div>
            <div class="pb-4">
                <p>Search On Test Cases</p>
                <Search
                    request="/test_cases/{projectID}/search/"
                    objects={testSuite.test_cases}
                    objectsCopy={testSuiteCopy.test_cases}
                    on:message={handleSearch}
                />
            </div>
            <AddNewSection />
            <TestSuiteSections {projectID} testSuiteID={testSuite.id}/>
        </div>
    {/if}
{:else}
    <LoodingSpiner />
{/if}
<DeleteModal
    bind:showDeleteModal
    on:message={handleDelete}
    obj={thisTestCase}
    onRequest="/test_cases/detail"
/>

<svelte:head>
    <title>Test-Tracker | Test Suite Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        ul {
            margin: 0;
        }
        h1 {
            font-size: 1.5rem;
        }
        h3 {
            font-size: 20px;
        }
        .card_info {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 20px;
            margin-bottom: 20px;
        }
        .card_info p {
            font-size: 20px;
            font-weight: 700;
        }

        .test_case_card {
            position: relative;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .test_case_card a {
            text-decoration: none;
            color: #5a79b1;
            display: block;
            font-weight: 700;
        }
        .collapse_span {
            position: absolute;
            right: 30px;
            height: 30px;
            width: 30px;
            text-align: center;
            border-radius: 50%;
        }
        .test_case_info {
            margin-top: 10px;
            padding: 5px;
        }
        .collapse-style {
            margin-left: 25px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .collapse-style a {
            display: inline;
            color: #5a79b1;
            font-size: 17px;
        }
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            top:20px
        }
    </style>
</svelte:head>
