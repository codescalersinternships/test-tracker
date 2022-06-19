<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";

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
        members = memberResponse.data.data;
        testRuns = runsResponse.data.data;
        report = lastWeekReport.data.data;
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
            testRuns = response.data.data;
        } else if (member.length !== 0 && status.length === 0) {
            const response = await axios.get(
                `/test_runs/${projectID}/search/?member=${member}`,
                config
            );
            testRuns = response.data.data;
        } else {
            const response = await axios.get(
                `/test_runs/${projectID}/search/?member=${member}&status=${status.replace(
                    " ",
                    "_"
                )}`,
                config
            );
            testRuns = response.data.data;
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
                    <strong class="h4">Test Runs</strong>
                    <br />
                    -- There are <strong>{testRuns.length}</strong>
                    Test {testRuns.length === 1 ? "Run" : "Runs"}
                </div>
                <div class="pt-4">
                    <p>Search On Test Runs</p>
                    <div class="row align-items-end mb-4">
                        <div class="col-4">
                            <strong
                                ><label for="#select-user">Involve user</label
                                ></strong
                            >
                            <select
                                bind:value={member}
                                class="form-select mt-1"
                                aria-label="select-user"
                                id="select-user"
                            >
                                <option selected />
                                {#if members}
                                    {#each members as member}
                                        <option value={member.id}
                                            >{member.full_name}</option
                                        >
                                    {/each}
                                {/if}
                            </select>
                        </div>
                        <div class="col-4">
                            <strong
                                ><label for="#select-status">Status</label
                                ></strong
                            >
                            <select
                                bind:value={status}
                                class="form-select"
                                aria-label="select-status"
                                id="select-status"
                            >
                                <option selected />
                                <option value="not started">not started</option>
                                <option value="in progress">in progress</option>
                                <option value="completed">completed</option>
                            </select>
                        </div>
                        <div class="col-2 pb-1">
                            <button
                                type="button"
                                class="btn btn-outline-primary"
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
                                class="nav-link active"
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
                            {#if testRuns}
                                {#each testRuns as run}
                                    <div class="card card-style">
                                        <Dropdown>
                                            <li>
                                                <button
                                                    class="dropdown-item text-danger"
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
                                                <h5 class="card-title" style="color: #5a79b1;">
                                                    {#if run.assigned_user.first_name}
                                                        {run.assigned_user.first_name}-{run.title}
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
                                                            <p
                                                                class="text-muted"
                                                            >
                                                                <svg
                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                    width="20"
                                                                    height="20"
                                                                    fill="currentColor"
                                                                    class="bi bi-pause-circle svg"
                                                                    viewBox="0 0 16 16"
                                                                >
                                                                    <path
                                                                        d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
                                                                    />
                                                                    <path
                                                                        d="M5 6.25a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5zm3.5 0a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5z"
                                                                    />
                                                                </svg>
                                                                <strong
                                                                    >Not Started</strong
                                                                >
                                                            </p>
                                                        {:else if run.status === "in_progress"}
                                                            <p
                                                                class="text-muted"
                                                            >
                                                                <svg
                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                    width="20"
                                                                    height="20"
                                                                    fill="currentColor"
                                                                    class="bi bi-arrow-repeat svg"
                                                                    viewBox="0 0 16 16"
                                                                >
                                                                    <path
                                                                        d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"
                                                                    />
                                                                    <path
                                                                        fill-rule="evenodd"
                                                                        d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"
                                                                    />
                                                                </svg>
                                                                <strong
                                                                    >In Progress</strong
                                                                >
                                                            </p>
                                                        {:else if run.status === "completed"}
                                                            <p
                                                                class="text-muted"
                                                            >
                                                                <svg
                                                                    xmlns="http://www.w3.org/2000/svg"
                                                                    width="20"
                                                                    height="20"
                                                                    fill="currentColor"
                                                                    class="bi bi-check-circle svg"
                                                                    viewBox="0 0 16 16"
                                                                >
                                                                    <path
                                                                        d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
                                                                    />
                                                                    <path
                                                                        d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"
                                                                    />
                                                                </svg>
                                                                <strong
                                                                    >Completed</strong
                                                                >
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
                        <div
                            class="tab-pane fade"
                            id="ex1-tabs-2"
                            role="tabpanel"
                            aria-labelledby="ex1-tab-2"
                        >
                            <h5>Test run results for the past week</h5>
                            <hr />
                            <div class="card card-style">
                                <div class="card-body pb-4">
                                    <div class="row">
                                        <div class="col-3 report-graid">
                                            <span class="pass report-span-style"
                                                >{report.passed}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#7fb24b"
                                                >Passed</span
                                            >
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="fail report-span-style"
                                                >{report.failed}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#f1495d"
                                                >Failed</span
                                            >
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="skip report-span-style"
                                                >{report.skipped}</span
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
                                                >{report.not_run}</span
                                            >
                                            <span
                                                class="report-span-text"
                                                style="color:#A5b3C0"
                                                >Not Run</span
                                            >
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
                                    <div
                                        class="card mb-2"
                                        style="box-shadow: none;"
                                    >
                                        <div class="card-body pt-0 pb-1">
                                            <p class="mb-1">Involve you</p>
                                            <span
                                                class="report-details report-span-style"
                                                >{report.not_started_test_runs
                                                    .involve_you}</span
                                            >
                                        </div>
                                    </div>
                                    <div
                                        class="card mb-2"
                                        style="box-shadow: none;"
                                    >
                                        <div class="card-body pt-0 pb-1">
                                            <p class="mb-1">
                                                Total not started
                                            </p>
                                            <span
                                                class="report-details report-span-style"
                                                >{report.not_started_test_runs
                                                    .total_not_started}</span
                                            >
                                        </div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div
                                        class="card mb-2"
                                        style="box-shadow: none;"
                                    >
                                        <div class="card-body pt-0 pb-1">
                                            <p class="mb-1">Involve you</p>
                                            <span
                                                class="report-details report-span-style"
                                                >{report.in_progress_test_runs
                                                    .involve_you}</span
                                            >
                                        </div>
                                    </div>
                                    <div
                                        class="card mb-2"
                                        style="box-shadow: none;"
                                    >
                                        <div class="card-body pt-0 pb-1">
                                            <p class="mb-1">
                                                Total in progress
                                            </p>
                                            <span
                                                class="report-details report-span-style"
                                                >{report.in_progress_test_runs
                                                    .total_in_progress}</span
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
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            width: 35px; 
            top:20px
        }
    </style>
</svelte:head>
