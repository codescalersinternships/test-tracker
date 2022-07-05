<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from 'svelte';
    import AreaSelect from "./AreaSelect.svelte";
    import Alert from "./Alert.svelte";
    import Input from "./Input.svelte";
    import Radio from "./Radio.svelte";
    import TextArea from "./TextArea.svelte";
    import { postNewObject } from "../../healpers/postNewObject"
    import { 
        claerFields, 
        validateFields 
    } from "../../healpers/validateFields"
    import {
        loadTestSuiteBasedOnProjectID,
        loadTestPlanBasedOnProjectID,
        loadProjectRequirementsBasedOnProjectID,
    } from "../../healpers/api"

    export let data, current;
    const dispatch = createEventDispatcher();

    let showAlert, 
        message, 
        _class, 
        testPlans, 
        projectRequirements,
        testSuites,
        selectedSuites = [];
    
    let nodes = [];

    function logger(_class_, _message_) {
        showAlert = true;
        _class = _class_;
        message = _message_;
    };

    function selectTestSuite(e, suite){
        const node = e.currentTarget;
        selectedSuites = selectedSuites;
        
        node.disabled = true;
        if(!selectedSuites.some(_suite => _suite.id === suite.id)){
            selectedSuites.push(suite);
            data.fields.test_suites = selectedSuites;
        }
        node.classList.add("selected-suite");
        nodes.push(node)
    }

    onMount(async () => {
        testPlans = await loadTestPlanBasedOnProjectID(
            data.fields.project_id
        );
        projectRequirements = await loadProjectRequirementsBasedOnProjectID(
            data.fields.project_id
        );
        testSuites = await loadTestSuiteBasedOnProjectID(
            data.fields.project_id
        );
    });

    function handleNodes(_nodes){
        for (const node of _nodes) {
                node.disabled = false;
                node.classList.remove("selected-suite");
            }
        nodes = [];
    }

    const postObject = async function(e){
        const response = await postNewObject(e, data);
        _class = response.class;
        message = response.message;
        if (response.data) {
            setTimeout(() => {
                handleCloseModalClick();
                response.data.type = data.obj;
                handleNodes(nodes);
                dispatch('message', {
                    obj: response
                });
            }, 1500);
        }
        logger(_class, message);
    }

    async function handleCloseModalClick() {
        claerFields(data);
        data.showPostModal = false;
        showAlert = false;
        selectedSuites = [];
        handleNodes(nodes);
    }

</script>
<div class="modal update-modal" tabindex="-1"
    style={`display: ${data.showPostModal ? "block" : "none"};`}
    >
    <div class:modal-xl="{current === 'test_case' || current === 'test_run'}" 
        class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                <div class="modal-header">
                    <h5>{data.message}</h5>
                </div>
                <form>
                    <Alert {showAlert} {message} {_class}/>
                    <Input 
                        bind:value={data.fields.title} 
                        id={"project-title"} 
                        title={"title"} 
                        type={"text"}
                    />
                    {#if data.obj == 'project'}
                        <TextArea 
                            bind:value={data.fields.short_description} 
                            title={'Short Description'}
                        />
                    {:else if data.obj == 'test_plan'}
                        <div class="form-group p-2 mb-2">
                            <Radio 
                                bind:group={data.fields.type}
                                value="template"
                                id="radio-template"
                                title="Create With Default Templates"
                            />
                            <Radio 
                                bind:group={data.fields.type}
                                value="blank"
                                id="radio-blank"
                                title="Create With Custom Templates"
                            />
                        </div>
                    {:else if data.obj == 'test_plan_content_area'}
                        <TextArea
                            bind:value={data.fields.content}
                            title="Content Area Description"
                        />
                    {:else if data.obj == "requirement"}
                        <TextArea
                            bind:value={data.fields.description}
                            title="Description"
                        />
                    {:else if data.obj == "test_suite"}
                        {#if testPlans && testPlans.length > 0}
                            <AreaSelect
                                objects={testPlans}
                                bind:value={data.fields.test_plan}
                                id={"select-testsuite-plan"}
                                labelTitle={"Test Plan"}
                            />
                        {:else}
                            <Alert 
                                showAlert = {true} 
                                message = {"You have to create at least one test plan, before creating a test suite."} 
                                _class = {"warning"}
                            />
                        {/if}
                    {:else if data.obj == 'test_case'}
                        <TextArea
                            bind:value={data.fields.description}
                            title="Description"
                        />
                        <TextArea
                            bind:value={data.fields.test_steps}
                            title="Test Steps"
                        />
                        <TextArea
                            bind:value={data.fields.expected_result}
                            title="Expected Result"
                        />
                        {#if projectRequirements && projectRequirements.length > 0}
                            <AreaSelect
                                objects={projectRequirements}
                                bind:value={data.fields.requirement}
                                id={"select-testcase-requirement"}
                                labelTitle={"Verify requirement"}
                            />
                        {/if}
                    {:else if data.obj == 'test_run'}
                        {#if testPlans && testPlans.length > 0}
                            <AreaSelect
                                objects={testPlans}
                                bind:value={data.fields.test_plan}
                                id={"select-testsuite-plan"}
                                labelTitle={"Test Plan"}
                            />
                        {/if}
                        {#if selectedSuites && selectedSuites.length > 0}
                            <div class="modal-header">
                                <h5>Selected Test Suites</h5>
                            </div>
                            <div class="suites card-body row mt-4">
                                {#each selectedSuites as selectedSuite}
                                    <div class="col-3">
                                        <a href="/projects/{data.fields.project_id}/test-suites/{selectedSuite.id}">
                                            {selectedSuite.title}
                                        </a>
                                    </div>
                                {/each}
                            </div>
                        {:else}
                            <Alert 
                                showAlert = {true} 
                                message = {"Please load test suites to create test run."} 
                                _class = {"warning"}
                            />
                        {/if}
                        <div class="select-suites text-center mb-3 mt-3">
                            <button
                                type="button"
                                class="btn plus-background text-light" 
                                data-mdb-toggle="modal" data-mdb-target="#SuiteModal"
                                >
                                Select test suites
                            </button>
                        </div>
                    {/if}
                </form>
                <div class="modal-footer">
                    <button 
                        type="button" 
                        class="btn btn-primary" 
                        data-mdb-dismiss="modal" 
                        on:click={handleCloseModalClick}>
                        Close
                    </button>
                    <button
                        disabled={!validateFields(data)}
                        class="btn btn-success" 
                        data-mdb-dismiss="modal" 
                        on:click={(e) => postObject(e)}>
                        Create
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="SuiteModal" tabindex="-1" aria-labelledby="SuiteModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-body">
                {#if testSuites && testSuites.length > 0}
                    {#each testSuites as suite}
                        <div class="card mb-3">
                            <button
                                class="text-dark suites-selected-button" 
                                on:click={(e) => selectTestSuite(e, suite)}>
                                <div class="card-body pb-2">
                                    <h5 class="card-title text-primary">
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
                            </button>
                        </div>
                    {/each}
                {:else}
                    <Alert 
                        showAlert = {true} 
                        message = {"There are no test suites available to use."} 
                        _class = {"info"}
                    />
                {/if}
            </div>
        </div>
    </div>
</div>

<svelte:head>
    <style>
        textarea {
            height: 150px; 
            max-height: 150px
        }
        .modal-xl {
            max-width: 1140px;
        }
        .suites{
            width: 98%;
            justify-content: center;
            align-items: center;
            display: flex;
            text-align: center;
            margin: 0 auto;
            color: #5271be;
            margin-bottom: 10px;
            box-shadow: 1px 0px 4px 1px #bdbdbd;
            font-size: 18px;
            font-weight: 500;
        }
    </style>
</svelte:head>