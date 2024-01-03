<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";

    import { statusFields } from "../../src/healpers/fields"
    import axios from "../healpers/axios";

    import NotStartedSVG from "../components/svg/NotStartedSVG.svelte";
    import InProgressSVG from "../components/svg/InProgressSVG.svelte";
    import CompletedSVG from "../components/svg/CompletedSVG.svelte";
    
    import Alert from "../components/ui/Alert.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import AreaSelect from "../components/ui/AreaSelect.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    
    import NavBar from "../components/NavBar.svelte";

    export let user;
    let members,
        status,
        member,
        projectID,
        testRuns,
        testRunsCopy,
        thisTestRun,
        report;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        let path = window.location.pathname;
        projectID = path.split("/")[2];

        const memberResponse = await axios.get("/members/all/", config);
        const runsResponse = await axios.get(
            `/test_runs/projects/${projectID}/`,
            config
        );
        const lastWeekReport = await axios.get(
            `/test_runs/projects/${projectID}/last_week_report/`,
            config
        );
        members = memberResponse.data.results
        testRuns = runsResponse.data.results
        report = lastWeekReport.data.results;
        testRunsCopy = testRuns;
    });

    async function setRun(run) {
        thisTestRun = run;
        showDeleteModal = true;
    }

    async function handleDelete(event) {
        const run = event.detail.obj;
        const indx = testRuns.findIndex((v) => v.id === run.id);
        testRuns = testRuns;
        testRuns.splice(indx, 1);
    }

    async function handleSearch() {
        if (member.length === 0 && status.length === 0) {
            testRuns = testRunsCopy;
        } else if (member.length === 0 && status.length !== 0) {
            const response = await axios.get(
                `/test_runs/${projectID}/search/?status=${status.replace(
                    " ",
                    "_"
                )}`,
                config
            );
            testRuns = response.data.results
        } else if (member.length !== 0 && status.length === 0) {
            const response = await axios.get(
                `/test_runs/${projectID}/search/?member=${member}`,
                config
            );
            testRuns = response.data.results
        } else {
            const response = await axios.get(
                `/test_runs/${projectID}/search/?member=${member}&status=${status.replace(
                    " ",
                    "_"
                )}`,
                config
            );
            testRuns = response.data.results
        }
    }
</script>

<section>
    {#if user}
        <NavBar projectView="true" 
            {user}
            on:message={
                (event) => {
                    if(event.detail.obj.data.type === "test_run"){
                        testRuns = testRuns;
                        testRuns.unshift(event.detail.obj.data);
                    }
                }
            }
        />
        <div class="container pt-4 pb-4">
            {#if testRuns}
                <div class="">
                    <strong class="h4 text-primary">Test Runs</strong>
                    <br />
                    -- There are <strong class="text-primary">{testRuns.length}</strong>
                    Test {testRuns.length === 1 ? "Run" : "Runs"}
                </div>
                <div class="pt-4">
                    <div class="row align-items-end mb-4">
                        <div class="col-4">
                            <AreaSelect
                                objects={members}
                                bind:value={member}
                                id={"select-user"}
                                labelTitle={"Involve user"}
                                user={true}
                            />
                        </div>
                        <div class="col-4">
                            <AreaSelect
                                objects={statusFields()}
                                bind:value={status}
                                id={"select-status"}
                                labelTitle={"Status"}
                                onClick={() => {}}
                            />
                        </div>
                        <div class="col-2 pb-4 ">
                            <button
                                type="button"
                                class="btn btn-outline-primary col-filter-run-btn"
                                on:click={handleSearch}
                            >
                                Search
                            </button>
                        </div>
                    </div>
                </div>
                <section class="section-tabs">
                    <ul class="nav nav-tabs mb-5" id="ex1" role="tablist">
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link nav-link-tab active"
                                id="ex1-tab-1"
                                data-mdb-toggle="tab"
                                href="#ex1-tabs-1"
                                role="tab"
                                aria-controls="ex1-tabs-1"
                                aria-selected="true">Test run list</a
                            >
                        </li>
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link nav-link-tab"
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
                            {#if testRuns}
                                {#each testRuns as run}
                                    <div class="card card-style">
                                        <Dropdown>
                                            <li>
                                                <button
                                                    class="dropdown-item setting-drop"
                                                    on:click={setRun(run)}>
                                                    Run
                                                </button>
                                            </li>
                                            <li>
                                                <button
                                                    class="dropdown-item text-danger drop-size plus-hover"
                                                    on:click={setRun(run)}>
                                                    Delete
                                                </button>
                                            </li>
                                        </Dropdown>
                                        <Link
                                            to="/projects/{projectID}/runs/{run.id}/"
                                            class="text-dark d-block text-decoration-none"
                                        >
                                            <div class="card-body pb-2">
                                                <h5 class="card-title text-primary">
                                                    {#if run.assigned_user && run.assigned_user.first_name}
                                                        @{run.assigned_user.full_name} - [{run.title}]
                                                    {:else}
                                                        {run.title}
                                                    {/if}
                                                </h5>
                                                <div class="row">
                                                    <div class="col-2">
                                                        <p class="text-muted">
                                                            Created: <strong
                                                                >{run.created}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-2">
                                                        {#if run.status === "not_started"}
                                                            <p class="text-muted">
                                                                <NotStartedSVG />
                                                                <strong>Not Started</strong>
                                                            </p>
                                                        {:else if run.status === "in_progress"}
                                                            <p class="text-muted">
                                                                <InProgressSVG />
                                                                <strong>In Progress</strong>
                                                            </p>
                                                        {:else if run.status === "completed"}
                                                            <p class="text-muted">
                                                                <CompletedSVG />
                                                                <strong>Completed</strong>
                                                            </p>
                                                        {/if}
                                                    </div>
                                                    <div class="col-2">
                                                        <p class="text-muted">
                                                            Test Cases <strong
                                                                >{run.total_test_cases}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-2">
                                                        <p class="text-muted">
                                                            Completed <strong
                                                                >{run.completed}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-1">
                                                        <p
                                                            style="display: table-caption;"
                                                            class="text-muted"
                                                        >
                                                            Passed <span
                                                                class="number pass"
                                                            /><strong
                                                                >{run.passed}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-1">
                                                        <p
                                                            style="display: table-caption;"
                                                            class="text-muted"
                                                        >
                                                            Failed <span
                                                                class="number fail"
                                                            /><strong
                                                                >{run.failed}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-1">
                                                        <p
                                                            style="display: table-caption;"
                                                            class="text-muted"
                                                        >
                                                            Skipped <span
                                                                class="number skip"
                                                            /><strong
                                                                >{run.skipped}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                    <div class="col-1">
                                                        <p
                                                            style="display: table-caption;width: 70px;"
                                                            class="text-muted"
                                                        >
                                                            Not-Run <span
                                                                class="number not_run"
                                                            /><strong
                                                                >{run.not_run}</strong
                                                            >
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </Link>
                                    </div>
                                {:else}
                                    <div class="col-12">
                                        <Alert 
                                            _class={'info'} 
                                            showAlert={true} 
                                            message={"There are no test runs yet, Try run test suite."} 
                                        />
                                    </div>
                                {/each}
                            {/if}
                        </div>
                        <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
                            <div class="row">
                                <div class="col-6">
                                    <h5>Filter test result based on weeks</h5>
                                    Test run results for the past week
                                </div>
                                <div class="col-6"></div>
                            </div>
                            <hr />
                            <div class="card card-style">
                                <div class="card-body pb-4">
                                    <div class="row">
                                        <div class="col-3 report-graid">
                                            <span class="pass report-span-style">
                                                {report.passed}
                                            </span>
                                            <span class="report-span-text" style="color:#7fb24b">
                                                Passed
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="fail report-span-style">
                                                {report.failed}
                                            </span>
                                            <span class="report-span-text" style="color:#f1495d">
                                                Failed
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="skip report-span-style">
                                                {report.skipped}
                                            </span>
                                            <span class="report-span-text" style="color:#f5a623;">
                                                Skipped
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="not_run report-span-style">
                                                {report.not_run}
                                            </span>
                                            <span class="report-span-text text-primary">
                                                Not Run
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br />
                            <div class="row">
                                <div class="col-6">
                                    <h5>Not started test runs</h5>
                                    <hr />
                                </div>
                                <div class="col-6">
                                    <h5>In progress test runs</h5>
                                    <hr />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-6">
                                    <div class="card mb-3 p-4">
                                        <div class="row">
                                            <div class="col-6">
                                                <p class="mb-1">Involve you</p>
                                                <span class="report-details report-span-style">
                                                    {report.not_started_test_runs.involve_you}
                                                </span>
                                            </div>
                                            <div class="col-6">
                                                <p class="mb-1">Total not started</p>
                                                <span class="report-details report-span-style">
                                                    {report.not_started_test_runs.total_not_started}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="card mb-3 p-4">
                                        <div class="row">
                                            <div class="col-6">
                                                <p class="mb-1">Involve you</p>
                                                <span class="report-details report-span-style">
                                                    {report.in_progress_test_runs.involve_you}
                                                </span>
                                            </div>
                                            <div class="col-6">
                                                <p class="mb-1">Total in progress</p>
                                                <span class="report-details report-span-style">
                                                    {report.in_progress_test_runs.total_in_progress}
                                                </span>
                                            </div>
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
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisTestRun}
        onRequest="/test_runs/projects/{projectID}/runs"
    />
</section>

<svelte:head>
    <title>Test-Tracker | Test runs</title>
    <style>
        .nav-style {
            width: 50%;
            text-align: center;
        }
        .card-style {
            border: 1px solid #dadada;
            margin-bottom: 15px;
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
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            width: 35px; 
            top:20px
        }
    </style>
</svelte:head>
