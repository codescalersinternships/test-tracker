<script>
    import { onMount } from "svelte";
    import { Router, Link } from "svelte-navigator";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import Search from "../components/Search.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";
    import CollapseSVG from "../components/svg/CollapseSVG.svelte";
    import Calendar from "../components/Calendar.svelte"; 

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let showDeleteModal = false;
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let testRunID = path.split("/")[4];

    let testRun,
    testSuites,
    testSuitesCopy,
    thisSuite,
    members,
    member,
    showAlert,
    message,
    _class;

    const today = new Date;

    onMount(async () => {
        const testRunDetails = await axios.get(
            `/test_runs/projects/${projectID}/runs/${testRunID}/`,
            config
        );
        const memberResponse = await axios.get(`members/project/${projectID}/members/`, config);
        testRun = testRunDetails.data.data;
        members = memberResponse.data.data;
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

    async function setAssignedUser(){
        if (member){
            if (testRun.assigned_user && testRun.assigned_user.id === member){
                message = "Already selected.";
                _class = "danger";
                showAlert = true;
            } else {
                const response = await axios.put(
                    `/test_runs/projects/${projectID}/set-user/${testRunID}/?assigned_user=${member}`,
                    [], config
                );
                if (response.data.status === 201){
                    testRun.assigned_user = response.data.data.assigned_user;
                    message = response.data.message;
                    _class = "success";
                    showAlert = true;
                    setTimeout(() => {
                        message = "";
                        _class = "";
                        showAlert = false;
                    }, 3000);
                } else {
                    message = response.data.message;
                    _class = "danger";
                    showAlert = true;
                }
            }
        }
    }
</script>

<section>
    {#if user}
        <NavBar projectView="true" {user} />
        <Alert {showAlert} {message} {_class}/>
        <div class="container pt-4 pb-4">
            {#if testRun}
                <div class="row">
                    <div class="col-11">
                        <p class="h4 mb-2">
                            Test Runs |
                            <strong class="h4 text-primary">{testRun.title}</strong>
                        </p>
                        <p class="text-muted">
                            -- Contains a total of <strong class="text-primary"
                                >{testSuites.length}</strong
                            >
                            {testSuites.length === 1 ? "test" : "tests"} suites
                        </p>
                    </div>
                    <div class="col-1">
                        <Router>
                            <Link to="/projects/{projectID}/runs/{testRunID}/run/" 
                                class="btn btn-primary ml-2 text-light">
                                Run
                            </Link>
                        </Router>
                    </div>
                </div>
                <div class="row mb-4">
                    <div class="col-6">
                        <div
                            class="card mb-3 text-center btn-primary"
                            style="font-size: 20px;font-weight: 600;"
                        >
                            <div class="card-body pb-2">
                                <p>Created : {testRun.created}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div
                            class="card mb-3 text-center btn-primary"
                            style="font-size: 20px;font-weight: 600;"
                        >
                            <div class="card-body pb-2">
                                <p>Updated : {testRun.modified}</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card card_info">
                            <p>Status</p>
                            <div class="card-body p-0 text-center">
                                {testRun.status.replace("_", " ").toUpperCase()}
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card card_info">
                            <p>Completed</p>
                            <div class="card-body p-0 text-center">
                                {testRun.completed}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mb-4">
                    <div class="col-6 pt-2">
                        <p class="pb-1 m-1">
                            <strong>Search on test runs</strong>
                        </p>
                        <Search
                            request="/test_suites/{projectID}/search/"
                            objects={testSuites}
                            objectsCopy={testSuitesCopy}
                            on:message={handleSearch}
                        />
                    </div>
                    <div class="col-6 pt-2">
                        <p class="pb-1 m-1">
                            <strong>Assigned user</strong>
                        </p>
                        <div class="input-group">
                            <select
                                class="form-select input"
                                aria-label="select-user"
                                bind:value={member}
                                >
                                {#if testRun.assigned_user}
                                    <option value={testRun.assigned_user.id} selected>
                                        Assigned to | {testRun.assigned_user.full_name} | select to change
                                    </option>
                                {:else if members.length === 0}
                                    <option value={null}>Try to add new user to this project.</option>
                                {:else}
                                    <option value={null}>Select user</option>
                                    {#each members as member }
                                        <option value={member.id}>{member.full_name}</option>
                                    {/each}
                                {/if}
                            </select>
                            <button type="button" class="btn btn-outline-primary" 
                                on:click={setAssignedUser}>
                                Submit
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
                                aria-selected="true">Test suites</a
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
                        <div class="tab-pane fade show active" id="ex1-tabs-1" role="tabpanel"
                            aria-labelledby="ex1-tab-1" >
                            {#each testSuites as suite}
                                <div class="col-12">
                                    <div class="card test_case_card mb-5">
                                        <Dropdown>
                                            <li>
                                                <button class="dropdown-item text-danger drop-size plus-hover"
                                                    on:click={setSuite(
                                                        suite
                                                    )}>Delete
                                                </button>
                                            </li>
                                        </Dropdown>
                                        <a data-mdb-toggle="collapse" href="#collapse-{suite.id}" role="button" 
                                            aria-expanded="false"
                                            aria-controls="collapse-{suite.id}"
                                            class="h5 text-primary">
                                            {suite.title}
                                        </a>

                                        <div class="card test_case_info">
                                            <a class="collapse_span" data-mdb-toggle="collapse" href="#collapse-{suite.id}"
                                                role="button" aria-expanded="false" aria-controls="collapse-{suite.id}">
                                                <CollapseSVG />
                                            </a>
                                            <div class="row" style="margin-left: 10px;">
                                                <div class="col-3">
                                                    <small>Created on</small>
                                                </div>
                                                <div class="col-3">
                                                    <small>Updated on</small>
                                                </div>
                                                <div class="col-3">
                                                    <small>Total test cases</small>
                                                </div>
                                                <div class="col-3">
                                                    <small>Test Plan</small>
                                                </div>

                                                <div class="col-3">
                                                    <strong>
                                                        <small>
                                                            {suite.created}
                                                        </small>
                                                    </strong>
                                                </div>
                                                <div class="col-3">
                                                    <strong>
                                                        <small>
                                                            {suite.modified}
                                                        </small>
                                                    </strong>
                                                </div>
                                                <div class="col-3">
                                                    <strong>
                                                        <small>
                                                            {suite.number_of_test_cases}
                                                        </small>
                                                    </strong>
                                                </div>
                                                {#if suite.test_plan.title}
                                                    <div class="col-3">
                                                        <strong>
                                                            <a href="/projects/{testRun.project_id}/test-plans/{suite.test_plan.id}/">
                                                                {#if suite.test_plan.title}
                                                                    <small>
                                                                        {
                                                                            suite.test_plan.title.length > 25 
                                                                            ? suite.test_plan.title.slice(0,25) +".."
                                                                            : suite.test_plan.title
                                                                        }
                                                                    </small>
                                                                {/if}
                                                            </a>
                                                        </strong>
                                                    </div>
                                                {:else}
                                                    <p>There are no plans</p>
                                                {/if}
                                            </div>
                                            <div class="collapse collapse-style" id="collapse-{suite.id}">
                                                <div class="row">
                                                    <div class="col-3">
                                                        <small style="color:#7fb24b">Passed</small>
                                                    </div>
                                                    <div class="col-3">
                                                        <small style="color:#f1495d">Failed</small>
                                                    </div>
                                                    <div class="col-3">
                                                        <small style="color:#f5a623">Skipped</small>
                                                    </div>
                                                    <div class="col-3">
                                                        <small class="text-primary">Not Run</small>
                                                    </div>

                                                    <div class="col-3">
                                                        <strong>
                                                            <span class="number pass" />
                                                            <small >{suite.passed}</small >
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span class="number fail"/>
                                                            <small>{suite.failed}</small>
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span class="number skip"/>
                                                            <small>{suite.skipped}</small>
                                                        </strong>
                                                    </div>
                                                    <div class="col-3">
                                                        <strong>
                                                            <span class="number not_run"/>
                                                            <small>{suite.not_run}</small>
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
                        <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
                            <div class="card card-style">
                                <div class="card-body pb-4">
                                    <div class="row">
                                        <div class="col-3 report-graid">
                                            <span class="pass report-span-style">
                                                {testRun.passed}
                                            </span>
                                            <span class="report-span-text" style="color:#7fb24b">
                                                Passed
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="fail report-span-style">
                                                {testRun.failed}
                                            </span>
                                            <span class="report-span-text" style="color:#f1495d">
                                                Failed
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="skip report-span-style">
                                                {testRun.skipped}
                                            </span>
                                            <span class="report-span-text" style="color:#f5a623">
                                                Skipped
                                            </span>
                                        </div>
                                        <div class="col-3 report-graid">
                                            <span class="btn-primary report-span-style">
                                                {testRun.not_run}
                                            </span>
                                            <span class="report-span-text text-primary">
                                                Not Run
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <Calendar {today}/>
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
/>
<svelte:head>
    <title>Test-Tracker | Test runs</title>
    <style>
        .dropdowncustom{
            position: absolute;
            font-size: 0!important;
            right: 0;
            top: 20px;
        }
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
            border-radius: 0px;
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
    </style>
</svelte:head>
