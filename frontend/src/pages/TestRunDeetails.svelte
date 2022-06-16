<script>
    import { onMount } from "svelte";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Search from "../components/Search.svelte";

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let showDeleteModal = false;
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let testRunID = path.split("/")[4];

    let testRun, testSuites, testSuitesCopy, thisSuite;

    onMount(async () => {
        const testRunDetails = await axios.get(
            `/test_runs/projects/${projectID}/runs/${testRunID}/`,
            config
        );
        testRun = testRunDetails.data.data;
        testSuites = testRun.test_suites;
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

<section>
    {#if user}
        <NavBar projectView="true" {user} />
        <div class="container pt-4 pb-4">
            {#if testRun}
                <div class="">
                    <p class="h4 mb-2">
                        Test Runs |
                        <strong class="h4 title">{testRun.title}</strong>
                    </p>
                    <p class="text-muted">
                        -- Contains a total of <strong class="text-dark"
                            >{testSuites.length}</strong
                        >
                        {testSuites.length === 1 ? "test" : "tests"}
                    </p>
                </div>
                <div class="row mb-4">
                    <div class="col-6">
                        <div
                            class="card mb-3 text-center"
                            style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
                        >
                            <div class="card-body pb-2">
                                <p>Created : {testRun.created}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div
                            class="card mb-3 text-center"
                            style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;"
                        >
                            <div class="card-body pb-2">
                                <p>Updated : {testRun.modified}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card_info">
                            <p>Status</p>
                            <div class="card-body p-0 text-center">
                                {testRun.status.replace("_", " ").toUpperCase()}
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card_info">
                            <p>Completed</p>
                            <div class="card-body p-0 text-center">
                                {testRun.completed}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mb-4">
                    <p>Search Suites</p>
                    <Search
                        request="/test_suites/{projectID}/search/"
                        objects={testSuites}
                        {config}
                        objectsCopy={testSuitesCopy}
                        on:message={handleSearch}
                    />
                </div>
                <section class="section-tabs">
                    <ul class="nav nav-tabs mb-5" id="ex1" role="tablist">
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link active"
                                id="ex1-tab-1"
                                data-mdb-toggle="tab"
                                href="#ex1-tabs-1"
                                role="tab"
                                aria-controls="ex1-tabs-1"
                                aria-selected="true">Test suites</a
                            >
                        </li>
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link"
                                id="ex1-tab-2"
                                data-mdb-toggle="tab"
                                href="#ex1-tabs-2"
                                role="tab"
                                aria-controls="ex1-tabs-2"
                                aria-selected="false">Reports</a
                            >
                        </li>
                    </ul>

                    <!-- Tabs content -->
                    <div class="tab-content" id="ex1-content">
                        <div
                            class="tab-pane fade show active"
                            id="ex1-tabs-1"
                            role="tabpanel"
                            aria-labelledby="ex1-tab-1"
                        >
                            {#each testSuites as suite}
                                <div class="col-12">
                                    <div class="test_case_card">
                                        <div
                                            class="dropdown p-1"
                                            style="position: absolute;font-size: 0!important;right: 0; top: 20px;"
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
                                                        on:click={setSuite(
                                                            suite
                                                        )}>Delete</button
                                                    >
                                                </li>
                                            </ul>
                                        </div>
                                        <a
                                            data-mdb-toggle="collapse"
                                            href="#collapse-{suite.id}"
                                            role="button"
                                            aria-expanded="false"
                                            aria-controls="collapse-{suite.id}"
                                        >
                                            {suite.title}
                                        </a>

                                        <div class="test_case_info">
                                            <a
                                                class="collapse_span"
                                                data-mdb-toggle="collapse"
                                                href="#collapse-{suite.id}"
                                                role="button"
                                                aria-expanded="false"
                                                aria-controls="collapse-{suite.id}"
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
                                            <div
                                                class="row"
                                                style="margin-left: 10px;"
                                            >
                                                <div class="col-3">
                                                    <small>Created on</small>
                                                </div>
                                                <div class="col-3">
                                                    <small>Updated on</small>
                                                </div>
                                                <div class="col-3">
                                                    <small
                                                        >Total test cases</small
                                                    >
                                                </div>
                                                <div class="col-3">
                                                    <small>Test Plan</small>
                                                </div>

                                                <div class="col-3">
                                                    <strong
                                                        ><small
                                                            >{suite.created}</small
                                                        ></strong
                                                    >
                                                </div>
                                                <div class="col-3">
                                                    <strong
                                                        ><small
                                                            >{suite.modified}</small
                                                        ></strong
                                                    >
                                                </div>
                                                <div class="col-3">
                                                    <strong
                                                        ><small
                                                            >{suite.number_of_test_cases}</small
                                                        ></strong
                                                    >
                                                </div>
                                                {#if suite.test_plan.title}
                                                    <div class="col-3">
                                                        <strong>
                                                            <a
                                                                href="/projects/{testRun.project_id}/test-plans/{suite
                                                                    .test_plan
                                                                    .id}/"
                                                            >
                                                                {#if suite.test_plan.title}
                                                                    <small>
                                                                        {suite
                                                                            .test_plan
                                                                            .title
                                                                            .length >
                                                                        25
                                                                            ? suite.test_plan.title.slice(
                                                                                  0,
                                                                                  25
                                                                              ) +
                                                                              ".."
                                                                            : suite
                                                                                  .test_plan
                                                                                  .title}
                                                                    </small>
                                                                {/if}
                                                            </a>
                                                        </strong>
                                                    </div>
                                                {:else}
                                                    <p>There are no plans</p>
                                                {/if}
                                            </div>
                                            <div
                                                class="collapse collapse-style"
                                                id="collapse-{suite.id}"
                                            >
                                                <div class="row">
                                                    <div class="col-3">
                                                        <small
                                                            style="color:#7fb24b"
                                                            >Passed</small
                                                        >
                                                    </div>
                                                    <div class="col-3">
                                                        <small
                                                            style="color:#f1495d"
                                                            >Failed</small
                                                        >
                                                    </div>
                                                    <div class="col-3">
                                                        <small
                                                            style="color:#f5a623;"
                                                            >Skipped</small
                                                        >
                                                    </div>
                                                    <div class="col-3">
                                                        <small
                                                            style="color:#5a79b1"
                                                            >Not Run</small
                                                        >
                                                    </div>

                                                    <div class="col-3">
                                                        <strong>
                                                            <span
                                                                class="number pass"
                                                            />
                                                            <small
                                                                >{suite.passed}</small
                                                            >
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span
                                                                class="number fail"
                                                            />
                                                            <small
                                                                >{suite.failed}</small
                                                            >
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span
                                                                class="number skip"
                                                            />
                                                            <small
                                                                >{suite.skipped}</small
                                                            >
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span
                                                                class="number not_run"
                                                            />
                                                            <small
                                                                >{suite.not_run}</small
                                                            >
                                                        </strong>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            {:else}
                                <div class="col-12 pt-5">
                                    <p class="text-muted">
                                        -- There are no test suites yet
                                    </p>
                                </div>
                            {/each}
                        </div>
                        <div
                            class="tab-pane fade"
                            id="ex1-tabs-2"
                            role="tabpanel"
                            aria-labelledby="ex1-tab-2"
                        >
                            <div class="card card-style">
                                <div class="card-body pb-4">
                                    <div class="row">
                                        <div class="col-3 report-graid">
                                            <span class="pass report-span-style"
                                                >{testRun.passed}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#7fb24b"
                                                >Passed</span
                                            >
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="fail report-span-style"
                                                >{testRun.failed}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#f1495d"
                                                >Failed</span
                                            >
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="skip report-span-style"
                                                >{testRun.skipped}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#f5a623;"
                                                >Skipped</span
                                            >
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span
                                                class="not_run report-span-style"
                                                >{testRun.not_run}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#5a79b1"
                                                >Not Run</span
                                            >
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
</section>
<DeleteModal
    bind:showDeleteModal
    on:message={handleDelete}
    obj={thisSuite}
    onRequest="/test_suites/{projectID}/actions"
    {config}
/>

<svelte:head>
    <title>Test-Tracker | Test runs</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        .nav-style {
            width: 50%;
            text-align: center;
        }
        .card-style {
            border: 1px solid #dadada;
            margin-bottom: 15px;
        }
        .svg {
            color: #5a79b1;
            margin-bottom: 3px;
        }
        .report-span-style {
            align-items: center;
            border-radius: 20px;
            color: #fff;
            display: flex;
            font-weight: bold;
            height: 40px;
            justify-content: center;
            line-height: 1;
            max-width: 70px;
            min-width: 70px;
        }
        .report-graid {
            align-items: center;
            display: flex;
            text-decoration: none;
        }
        .report-span-text {
            display: block;
            font-size: 1.57em;
            font-weight: bold;
            padding: 0 0 5px 0;
            margin-left: 10px;
        }
        .pass {
            background-color: #7fb24b;
        }
        .fail {
            background-color: #f1495d;
        }
        .skip {
            background-color: #f5a623;
        }
        .not_run {
            background-color: #5a79b1;
        }
        .report-details {
            background-color: #549dfa;
        }
        .number {
            display: inline-block;
            height: 8px;
            width: 8px;
            margin: 0px 5px 0.8px 0;
            border-radius: 50%;
        }
        .card_info {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .card_info p {
            font-size: 20px;
            font-weight: 700;
        }
        .test_case_card {
            position: relative;
            background-color: #f5f5f5;
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
        .collapse_span:hover {
            box-shadow: 0px 1px 4px 1px #d0d0d0;
            background: #f5f5f5;
        }
        .test_case_info {
            margin-top: 10px;
            background: #fcfcfc;
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
    </style>
</svelte:head>
