<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte"
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte"
    import TextArea from "../components/ui/TextArea.svelte"

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let testRunID = path.split("/")[4];
    let testRun, loading, testCases, testCase, comment;

    onMount(async () => {
        loading = true;
        const testCasesResponse = await axios.get(
            `/test_runs/projects/${projectID}/runs/${testRunID}/cases/`,
            config
        );
        const testRunDetails = await axios.get(
            `/test_runs/projects/${projectID}/runs/${testRunID}/`,
            config
        );
        testCases = testCasesResponse.data.data;
        testRun = testRunDetails.data.data;
        testCase = testCases[0];
        loading = false;
    });
</script>
<section>
    {#if user}
        <NavBar projectView="true" {user} />
        <!-- <Alert {showAlert} {message} {_class}/> -->
        <div class="container pt-4 pb-4">
            {#if loading}
                <LoodingSpiner />
            {:else}
                <div class="col-12">
                    <p class="h4 mb-2">
                        Test Runs |
                        <strong class="h4 title">{testRun.title}</strong>
                    </p>
                    <p class="text-muted">
                        Running all remaining tests
                    </p>
                </div>
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
                <div class="card card-style">
                    <div class="card-body pb-4">
                        <div class="title-suite p-2">
                            <h4>Test suite: <span class="title">{testCase.test_suite}</span></h4>
                        </div>
                        <div class="table-content p-2">
                            <h6>Number</h6>
                            <span class="title f-18">{testCase.testcase_title}</span>
                        </div>
                        <div class="table-content p-2">
                            <h6>Title</h6>
                            <span class="title f-18">{testCase.title}</span>
                        </div>
                        <div class="table-content p-2">
                            <h6>Description</h6>
                            <span class="title f-18">{testCase.description}</span>
                        </div>
                        <div class="table-content p-2">
                            <h6>Test steps</h6>
                            <span class="title f-18">{testCase.test_steps}</span>
                        </div>
                        <div class="table-content p-2">
                            <h6>Expected results</h6>
                            <span class="title f-18">{testCase.expected_result}</span>
                        </div>
                        <div class="table-content p-2">
                            <h6>Actual result / comments</h6>
                            <textarea bind:value={comment} class="form-control mt-3"></textarea>
                        </div>
                    </div>
                </div>
                <div class="card card-style">
                    <div class="card-body pb-4">
                        <div class="row">
                            <div class="col-4">
                                <button
                                    type="button"
                                    class="btn btn-custom pass"
                                    data-mdb-dismiss="modal"
                                    >
                                    Pass
                                </button>
                            </div>
                            <div class="col-4">
                                <button
                                    type="button"
                                    class="btn btn-custom skip"
                                    >
                                    Skip
                                </button>
                            </div>
                            <div class="col-4">
                                <button
                                    type="button"
                                    class="btn btn-custom fail"
                                    >
                                    Fail
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
</section>
<svelte:head>
    <title>Test-Tracker | Test runs</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
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
        .not_run {
            background-color: #5a79b1;
        }
        .f-18{
            font-size: 18px!important;
        }
        .btn-custom{
            border-radius: 20px;
            color: #fff;
            font-size: 17px;
            font-weight: 900;
            width: 100%;
        }
        .btn:hover {
            color: #fff !important;
        }
    </style>
</svelte:head>
