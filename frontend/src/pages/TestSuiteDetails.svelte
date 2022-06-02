<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"

    import snarkdown from 'snarkdown'

    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    let testSuite, testSuiteCopy, projectID, suiteID, thisTestCase;
    let show = false;

    onMount(async () => {
        // Loading test suite
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        suiteID = path.split("/")[4];
        try {
            const responseSuites = await axios.get(`test_suites/${projectID}/actions/${suiteID}/`, config);
            testSuite = responseSuites.data.data;
            testSuiteCopy = testSuite;
        } catch (error) {
            if (error.response.status == 404) {
                window.location.href = '/not-found/'
            }
            
        }
    });

    async function handleSearch(event) {
        const searchTestCase = event.detail.objects;
        testSuite.test_cases = searchTestCase;
    }

    function setTestCase(testCase) {
        thisTestCase = testCase
        show = true;
    }

    async function handleDelete(event) {
        const testCase = event.detail.obj;
        const indx = testSuite.test_cases.findIndex(v => v.id === testCase.id);
        testSuite = testSuite;
        testSuite.test_cases.splice(indx, 1);
    }

</script>

<svelte:head>
    <title>Test-Tracker | Test Suite Detail</title>
    <style>
        ul{
            margin: 0;
        }
        h1{
            font-size: 1.5rem;
        }
        h3 {
            font-size: 20px;
        }
        .card_info{
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
        .card_info p{
            font-size: 20px;
            font-weight: 700;
        }

        .test_case_card{
            position: relative;
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .test_case_card a{
            text-decoration: none;
            color: #5a79b1;
            display: block;
            font-weight: 700;
        }
        .collapse_span{
            position: absolute;
            right: 30px;
            height: 30px;
            width: 30px;
            text-align: center;
            border-radius: 50%;
        }
        .collapse_span:hover{
            box-shadow: 0px 1px 4px 1px #d0d0d0;
            background: #f5f5f5;
        }
        .test_case_info{
            margin-top: 10px;
            background: #fcfcfc;
            padding: 5px;
        }
        .collapse-style{
            margin-left: 25px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .collapse-style a{
            display: inline;
            color: #5a79b1;
            font-size: 17px;
        }
    </style>
</svelte:head>


{#if user}
    <NavBar projectView="true" user={user}/>
    {#if testSuite}
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5">
                    Test suites: {testSuite.title}
                </p>
                <p class="text-muted">
                    There are <strong>{testSuite.number_of_test_cases}</strong> test {testSuite.number_of_test_cases === 1 ? 'case' : 'cses'}
                </p>
            </div>
            <div class="row mb-4">
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Created : {testSuite.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Updated : {testSuite.modified}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card_info">
                        <p>Associated test plan</p>
                        {#if testSuite.test_plan}
                            <a href="/projects/{projectID}/test-plans/{testSuite.test_plan.id}" 
                                class="text-decoration-none">
                                <div class="card-body p-0 text-center">
                                    {testSuite.test_plan.title}
                                </div>
                            </a>
                        {:else}
                            <p class="text-muted">
                                No associated plan
                            </p>
                        {/if}
                    </div>
                </div>
            </div>
            <div class="pb-4">
                <p>
                    Search On Test Cases
                </p>
                <Search request="/test_cases/{projectID}/search/" objects={testSuite.test_cases} 
                    config={config} objectsCopy={testSuiteCopy.test_cases} on:message={handleSearch}/>
            </div>
            <div class="pb-1">
                <p class="text-muted">
                    Test Cases
                </p>
            </div>
            <div class="row">
                {#each testSuite.test_cases as test_case }
                    <div class="col-12">
                        <div class="test_case_card">
                            <div class="dropdown p-1" style="position: absolute;font-size: 0!important;right: 0; top: 20px;">
                                <a
                                    class="dropdown-toggle"
                                    id="dropdownMenuButton"
                                    data-mdb-toggle="dropdown"
                                    aria-expanded="false"
                                    >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                                        <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                    </svg>
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                    <li>
                                        <button class="dropdown-item text-danger" on:click={setTestCase(test_case)}>Delete</button>
                                    </li>
                                </ul>
                            </div>
                            <a
                                data-mdb-toggle="collapse"
                                href="#collapse-{test_case.id}"
                                role="button"
                                aria-expanded="false"
                                aria-controls="collapse-{test_case.id}"
                                >
                                {test_case.testcase_title}-{test_case.title}
                            </a>

                            <div class="test_case_info">
                                <a class="collapse_span"
                                    data-mdb-toggle="collapse"
                                    href="#collapse-{test_case.id}"
                                    role="button"
                                    aria-expanded="false"
                                    aria-controls="collapse-{test_case.id}"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67z"/>
                                    </svg>
                                </a>
                                <div class="row" style="margin-left: 10px;">
                                    <div class="col-3"><small>Updated on</small></div>
                                    <div class="col-3"><small>Last saved by</small></div>
                                    <div class="col-6"><small>Associated requirements</small></div>

                                    <div class="col-3"><strong><small>{test_case.modified}</small></strong></div>
                                    <div class="col-3">
                                        <strong><small>
                                            <a style="font-size: 15px;" href="/members/{test_case.last_saved.id}">@{test_case.last_saved.full_name}</a>
                                        </small></strong></div>
                                    <div class="col-6">
                                        <strong><small>
                                            {test_case.requirement.requirement_title}-{test_case.requirement.title} 
                                        </small></strong>
                                    </div>
                                </div>
                                <div class="collapse collapse-style" id="collapse-{test_case.id}">
                                    <small>Description:</small><br>
                                    <p>{test_case.description}</p>
                                    <small>Test steps:</small><br>
                                    {@html snarkdown(test_case.test_steps)}
                                    <small>Expected result</small><br>
                                    {@html snarkdown(test_case.expected_result)}
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/if}
{:else}
    <LoodingSpiner />
{/if}
<DeleteModal
    bind:show
    on:message={handleDelete}
    obj={thisTestCase}
    onRequest='/test_cases/detail'
    config={config}
/>