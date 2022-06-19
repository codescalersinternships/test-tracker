<script>
    import { onMount } from "svelte";
    import axios from "../../healpers/axios";
    import AreaSelect from "./AreaSelect.svelte";
    import AreaSelectWithButton from "./AreaSelectWithButton.svelte";
    import TextArea from "./TextArea.svelte";
    import Alert from "./Alert.svelte";
    import LoodingSpiner from "./LoodingSpiner.svelte";

    export let data;

    let requirementDocs,
        testPlans,
        projects = [];
    let loading = false;
    let loadReqDocs = false;

    let title, message, showAlert, _class;
    let config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    function validateFields() {
        for (const filed in data.fields) {
            if (data.fields[filed] === "" || data.fields[filed] === undefined) {
                return false;
            }
        }
        return true;
    }

    function claerFields() {
        for (const filed in data.fields) {
            data.fields[filed] = "";
        }
    }

    function logger(_class_, _message_) {
        showAlert = true;
        _class = _class_;
        message = _message_;
    }

    async function loadRequirementDocs() {
        if (data.fields.project_id === "defualt") {
            logger("danger", "Plese select project.");
            return;
        }
        try {
            loadReqDocs = true;
            const responseRequirements = await axios.get(
                `/requirements/projects/${data.fields.project_id}/get-all/`,
                config
            );
            requirementDocs = responseRequirements.data.data;
            if (!requirementDocs.length > 0) {
                logger(
                    "warning",
                    "No requirement document found for this project."
                );
            } else {
                showAlert = false;
            }
            loadReqDocs = false;
        } catch (err) {
            logger("danger", "Something went wrong.");
            loadReqDocs = false;
        }
    }

    async function loadTestPlans() {
        if (
            data.fields.project_id === "defualt" ||
            data.fields.project_id === ""
        ) {
            logger("danger", "Plese select project.");
            return;
        }

        try {
            loadReqDocs = true;
            const responsePlans = await axios.get(
                `/test_plan/${data.fields.project_id}/`,
                config
            );
            testPlans = responsePlans.data.data;
            if (!testPlans.length > 0) {
                logger("warning", "No Test Plans found for this project.");
            } else {
                showAlert = false;
            }
            loadReqDocs = false;
        } catch (err) {
            logger("danger", "Something went wrong.");
            loadReqDocs = false;
        }
    }

    onMount(async () => {
        const responseProjects = await axios.get(
            "/dashboard/projects/",
            config
        );
        projects = responseProjects.data.data;
        loading = false;
    });
    async function newObject(url, fields) {
        try {
            const response = await axios.post(url, fields, config);
            logger("success", response.data.message);
            setTimeout(() => {
                data["showPostModal"] = false;
                showAlert = false;
                claerFields();
            }, 1000);
        } catch (err) {
            logger("danger", err.response.data.message);
        }
    }

    async function handleObjects() {
        data.fields.title = title;
        const url = data.url;
        let _url;
        if (data.obj == "test_plan" || data.obj == "requirement_Doc") {
            _url = `${data.url}${data.fields.project_id}/`;
            data.url = _url;
        } else if (data.obj == "requirement") {
            if (data.fields.requirement_Doc === "defualt") {
                logger("danger", "Please select requirement do");
            }
            _url = `${data.url}projects/${data.fields.project_id}/requirement/${data.fields.requirement_Doc}/`;
            data.url = _url;
        } else if (data.obj == "test_suite") {
            _url = `${data.url}${data.fields.project_id}/`;
            data.url = _url;
        }
        if (validateFields()) {
            await newObject(data.url, data.fields);
        } else {
            logger("danger", "Please fill all required fields.");
        }
        data.url = url;
    }
</script>

<div
    class="modal update-modal"
    tabindex="-1"
    style={`display: ${data.showPostModal ? "block" : "none"};`}
>
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                <div class="modal-header">
                    <h5>{data.message}</h5>
                </div>
                <Alert {showAlert} {message} {_class} />
                <form>
                    {#if loading}
                        <LoodingSpiner />
                    {:else}
                        <div class="form-group p-2 pb-2">
                            <label for="content-title">Title</label>
                            <input
                                bind:value={title}
                                type="text"
                                class="form-control"
                                id="content-title"
                            />
                        </div>
                        {#if data.obj == "project"}
                            <TextArea
                                bind:value={data.fields.short_description}
                                title={"Short Description"}
                            />
                        {:else if data.obj == "test_plan"}
                            <AreaSelect
                                objects={projects}
                                bind:value={data.fields.project_id}
                                id={"select-project"}
                                labelTitle={"Project"}
                            />
                            <div class="form-group p-2 mb-4">
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        bind:group={data.fields.type}
                                        type="radio"
                                        id="flexRadioDefault1"
                                        value="template"
                                        checked
                                    />
                                    <label
                                        class="form-check-label"
                                        for="flexRadioDefault1"
                                        >Create With Default Templates</label
                                    >
                                </div>
                                <div class="form-check">
                                    <input
                                        class="form-check-input"
                                        bind:group={data.fields.type}
                                        type="radio"
                                        id="flexRadioDefault2"
                                        value="blank"
                                    />
                                    <label
                                        class="form-check-label"
                                        for="flexRadioDefault2"
                                        >Create With Custom Templates</label
                                    >
                                </div>
                            </div>
                        {:else if data.obj == "requirement_Doc"}
                            <AreaSelect
                                objects={projects}
                                bind:value={data.fields.project_id}
                                id={"select-requirement-doc-project"}
                                labelTitle={"Project"}
                            />
                        {:else if data.obj == "requirement"}
                            <TextArea
                                bind:value={data.fields.description}
                                title="Description"
                            />
                            <AreaSelectWithButton
                                {data}
                                onClickFunction={loadRequirementDocs}
                                objects={projects}
                                id={"select-project"}
                                labelTitle={"Project"}
                            />
                            {#if loadReqDocs}
                                <LoodingSpiner />
                            {:else if requirementDocs && requirementDocs.length > 0}
                                <AreaSelect
                                    objects={requirementDocs}
                                    bind:value={data.fields.requirement_Doc}
                                    id={"select-requirementdoc-requirement"}
                                    labelTitle={"Requirement Document"}
                                />
                            {/if}
                        {:else if data.obj == "test_suite"}
                            <AreaSelectWithButton
                                {data}
                                onClickFunction={loadTestPlans}
                                objects={projects}
                                id={"select-suite-project"}
                                labelTitle={"Project"}
                            />
                            {#if loadReqDocs}
                                <LoodingSpiner />
                            {:else if testPlans && testPlans.length > 0}
                                <AreaSelect
                                    objects={testPlans}
                                    bind:value={data.fields.test_plan}
                                    id={"select-testsuite-plan"}
                                    labelTitle={"Test Plan"}
                                />
                            {/if}

                            <!-- {:else if data.obj == 'test_case'}
                            <TextArea labelTitle="Description" 
                                bindValue={data.fileds.description} />
                            <TextArea labelTitle="Test Steps" 
                                bindValue={data.fileds.test_steps} />
                            <TextArea labelTitle="Expected Result" 
                                bindValue={data.fileds.expected_result} />
                                Verify requirement
                            <AreaSelect {objects} id={'select-requirement-case'} labelTitle={'Requirement'}/>
                            <AreaSelect {objects} id={'select-requirement-suite'} labelTitle={'Test Suite'}/> -->
                            <!-- 
                        {:else if data.obj == 'test_run'}
                            <AreaSelect {objects} id={'select-run-plan'} labelTitle={'Test Plan'}/>
                            <AreaSelect {objects} id={'select-run-project'} labelTitle={'Project'}/> -->
                        {/if}
                    {/if}
                </form>
                <div class="modal-footer">
                    <button
                        type="button"
                        class="btn btn-primary"
                        data-mdb-dismiss="modal"
                        on:click={() => (
                            (data["showPostModal"] = false), (showAlert = false)
                        )}>Close</button
                    >
                    <button
                        class="btn btn-success"
                        data-mdb-dismiss="modal"
                        on:click={handleObjects}>Create</button
                    >
                </div>
            </div>
        </div>
    </div>
</div>

<svelte:head>
    <style>
        textarea {
            height: 150px;
            max-height: 150px;
        }
    </style>
</svelte:head>
