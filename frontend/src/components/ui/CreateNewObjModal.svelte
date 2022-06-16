<script>
    import { onMount } from "svelte";
    import axios from "../../healpers/axios";
    import AreaSelect from "./AreaSelect.svelte"
    import TextArea from "./TextArea.svelte"
    import Alert from "./Alert.svelte"
    import LoodingSpiner from "./LoodingSpiner.svelte"

    export let data;

    let requirementDocs, projects = [];
    let loading = true;
    let loadReqDocs = false;

    let title, message, showAlert, _class;
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    async function loadRequirementDocs() {
        loadReqDocs = true;
        const responseRequirements = await axios.get(
            `/requirements/projects/${data.fields.project_id}/get-all/`,
            config
        );
        requirementDocs = responseRequirements.data.data;
        loadReqDocs = false;
    }
    
    onMount(async () => {
        const responseProjects = await axios.get("/dashboard/projects/", config);
        projects = responseProjects.data.data;
        loading = false;
    });

    async function createNewObject() {
        data.fields.title = title;
        const url = data.url
        if (data.obj == "test_plan" || data.obj == "requirement_Doc") {
            const _url = `${data.url}${data.fields.project_id}/`
            data.url = _url;
        } else if (data.obj == "requirement") {
            const _url = `${data.url}${data.fields.project_id}/requirement/${data.fields.requirement_Doc}/`
            data.url = _url;
        }
        console.log(data);
        try {
            const response = await axios.post(
                data.url, data.fields, config
            );
            showAlert = true;
            _class = "success";
            message = response.data.message;
            setTimeout(() => {
                data['showPostModal'] = false;
                showAlert = false;
            }, 1000);
        } catch (err) {
            showAlert = true;
            _class = "danger";
            message = err.response.data.message;
        }
        data.url = url;
    }
    
</script>

<div
    class="modal update-modal"
    tabindex="-1"
    style={`display: ${data.showPostModal ? "block" : "none"};`}
>    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                <div class="modal-header">
                    <h5>{data.message}</h5>
                </div>
                <Alert {showAlert} {message} {_class}/>
                <form>
                {#if loading}
                    <LoodingSpiner />
                    {:else}
                        <div class="form-group p-2 pb-2">
                            <label for="content-title">Title</label>
                            <input bind:value={title} type="text" class="form-control" id="content-title">
                        </div>
                        {#if data.obj == 'project'}
                            <TextArea bind:value={data.fields.short_description} />
                        {:else if data.obj == 'test_plan'}
                            <AreaSelect objects = {projects} bind:value={data.fields.project_id}
                                id={'select-project'} labelTitle={'Project'}/>
                            <div class="form-group p-2 mb-4">
                                <div class="form-check">
                                    <input class="form-check-input" bind:group={data.fields.type} type="radio" id="flexRadioDefault1" value="template" checked/>
                                    <label class="form-check-label" for="flexRadioDefault1">Create With Default Templates</label>
                                </div>
                                <div class="form-check">
                                    <input class="form-check-input" bind:group={data.fields.type} type="radio" id="flexRadioDefault2" value="blank"/>
                                    <label class="form-check-label" for="flexRadioDefault2">Create With Custom Templates</label>
                                </div>
                            </div>
                        {:else if data.obj == 'requirement_Doc'}
                            <AreaSelect objects = {projects} bind:value={data.fields.project_id}
                                id={'select-requirement-doc-project'} labelTitle={'Project'}/>
                        {:else if data.obj == 'requirement'}
                            <div class="d-flex flex-row align-items-center">
                                <div class="col-10">
                                    <AreaSelect objects = {projects} bind:value={data.fields.project_id}
                                        id={'select-project'} labelTitle={'Project'}/>
                                </div>
                                <div class="col-2">
                                    <button type="button" class="btn btn-primary mt-2" data-mdb-dismiss="modal"
                                        style="background-color: #bf4e62;" on:click={loadRequirementDocs}>
                                        <i class="fas fa-plus"></i>
                                    </button>
                                </div>
                            </div>
                            {#if loadReqDocs}
                                <LoodingSpiner />
                            {:else if requirementDocs && requirementDocs.length > 0}
                                <AreaSelect objects = {requirementDocs} bind:value={data.fields.requirement_Doc}
                                    id={'select-requirementdoc-requirement'} labelTitle={'Requirement Document'}/>
                            {:else}
                                <div class="alert alert-warning text-center">
                                    <small class="m-0">No Requirement Document Found, Select Another Project</small>
                                </div>
                            {/if}
                            <!-- <TextArea bind:value={data.fileds.description} /> -->
                        <!-- {:else if data.obj == 'test_suite'}
                            <AreaSelect {objects} id={'select-suite-project'} labelTitle={'Project'}/>
                            <AreaSelect {objects} id={'select-suite-plan'} labelTitle={'Test Plan'}/>
                        {:else if data.obj == 'test_case'}
                            <TextArea labelTitle="Description" 
                                bindValue={data.fileds.description} />
                            <TextArea labelTitle="Test Steps" 
                                bindValue={data.fileds.test_steps} />
                            <TextArea labelTitle="Expected Result" 
                                bindValue={data.fileds.expected_result} />
                            <AreaSelect {objects} id={'select-requirement-case'} labelTitle={'Requirement'}/>
                            <AreaSelect {objects} id={'select-requirement-suite'} labelTitle={'Test Suite'}/>
                        {:else if data.obj == 'test_run'}
                            <AreaSelect {objects} id={'select-run-plan'} labelTitle={'Test Plan'}/>
                            <AreaSelect {objects} id={'select-run-project'} labelTitle={'Project'}/> -->
                        {/if}
                    {/if}
                </form>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" 
                        on:click={() => (data['showPostModal'] = false)}>Close</button>
                    <button class="btn btn-success" data-mdb-dismiss="modal" 
                        on:click={createNewObject}>Create</button>
                </div>
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
    </style>
</svelte:head>
