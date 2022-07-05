<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Search from "../components/Search.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";

    import snarkdown from "snarkdown";

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

    function setTestCase(testCase) {
        thisTestCase = testCase;
        showDeleteModal = true;
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
                    Test Runs |
                    <strong class="h4 title">{testSuite.title}</strong>
                </p>
                <p class="text-muted">
                    There are <strong>{testSuite.number_of_test_cases}</strong>
                    test {testSuite.number_of_test_cases === 1
                        ? "case"
                        : "cses"}
                </p>
            </div>
            <div class="row mb-4">
                <div class="col-6">
                    <div
                        class="card mb-3 text-center"
                        style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Created : {testSuite.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div
                        class="card mb-3 text-center"
                        style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
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
                                class="text-decoration-none"
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
            {#if testSuite.test_cases && testSuite.test_cases.length}
                <div class="row pt-4">
                        {#each testSuite.test_cases as test_case}
                            <div class="col-12">
                                <div class="card test_case_card">
                                    <Dropdown>
                                        <li>
                                            <button
                                                class="dropdown-item text-danger drop-size plus-hover"
                                                on:click={setTestCase(test_case)}
                                                >Delete
                                            </button>
                                        </li>
                                    </Dropdown>
                                    <a
                                        data-mdb-toggle="collapse"
                                        href="#collapse-{test_case.id}"
                                        role="button"
                                        aria-expanded="false"
                                        aria-controls="collapse-{test_case.id}"
                                    >
                                        <span class="text-primary h5">
                                            {test_case.testcase_title}
                                        </span>
                                        <span class="text-muted h5">
                                            {test_case.title}
                                        </span>
                                    </a>

                                    <div class="test_case_info">
                                        <a
                                            class="collapse_span"
                                            data-mdb-toggle="collapse"
                                            href="#collapse-{test_case.id}"
                                            role="button"
                                            aria-expanded="false"
                                            aria-controls="collapse-{test_case.id}"
                                        >
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="25"
                                                height="30"
                                                fill="currentColor"
                                                class="bi bi-chevron-compact-down"
                                                viewBox="0 0 16 16"
                                            >
                                                <path
                                                    fill-rule="evenodd"
                                                    d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67z"
                                                />
                                            </svg>
                                        </a>
                                        <div class="row" style="margin-left: 10px;">
                                            <div class="col-3">
                                                <small>Updated on</small>
                                            </div>
                                            <div class="col-3">
                                                <small>Last saved by</small>
                                            </div>
                                            <div class="col-6">
                                                <small>Associated requirements</small>
                                            </div>

                                            <div class="col-3">
                                                <strong
                                                    ><small>{test_case.modified}</small
                                                    ></strong
                                                >
                                            </div>
                                            <div class="col-3">
                                                <strong
                                                    ><small>
                                                        <a
                                                            style="font-size: 15px;"
                                                            href="/members/{test_case
                                                                .last_saved.id}"
                                                            >@{test_case.last_saved
                                                                .full_name}</a
                                                        >
                                                    </small></strong
                                                >
                                            </div>
                                            {#if test_case.requirement}
                                                <div class="col-6">
                                                    <a href="/projects/{projectID}/requirements/{test_case.requirement.requirement_doc}">
                                                        <strong>
                                                            <small>
                                                                {test_case.requirement
                                                                .requirement_title}-{test_case
                                                                .requirement.title}
                                                            </small>
                                                        </strong>
                                                    </a>
                                                </div>
                                            {:else}
                                                <div class="col-6">
                                                    <small>No associated requirement</small>
                                                </div>
                                            {/if}
                                        </div>
                                        <div
                                            class="collapse collapse-style"
                                            id="collapse-{test_case.id}"
                                        >
                                            <small>Description:</small><br />
                                            <p>{test_case.description}</p>
                                            <small>Test steps:</small><br />
                                            {@html snarkdown(test_case.test_steps)}
                                            <small>Expected result</small><br />
                                            {@html snarkdown(test_case.expected_result)}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {/each}
                </div>
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
