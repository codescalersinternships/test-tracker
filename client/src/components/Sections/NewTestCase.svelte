<script>
    import TextArea from "../ui/TextArea.svelte";
    import Input from "../ui/Input.svelte";
    import AreaSelect from "../ui/AreaSelect.svelte";
    import { onMount } from "svelte";
    import { loadProjectRequirementsBasedOnProjectID, postNewTestCase } from "../../healpers/api"
    import ListAllTestSuiteTestCases from "./ListAllTestSuiteTestCases.svelte";
    import LoadingCompnent from "../ui/LoodingSpiner.svelte";
    import { newTestCaseFields } from "../../healpers/fields"
    import { createEventDispatcher } from 'svelte';
    import AddNewTestCase from "./AddNewTestCase.svelte"
    import { claerFields, validateFields } from "../../healpers/validateFields";

    export let section;
    export let testSuite;

    let form = newTestCaseFields();
    const dispatch = createEventDispatcher();


    let projectRequirements;
    let showTestCases = false;
    let showNormalForm = true;
    let isLoading = false;

    const types = [
        {id: "new", title: "New", selected: true},
        {id: "existing", title: "Existing", selected: false}   
    ]

    onMount(async () => {
        projectRequirements = await loadProjectRequirementsBasedOnProjectID(
            form.fields.project_id
        );
    });

</script>


<div class="card new-test-case">
    <AreaSelect
        objects={types}
        bind:value={form.fields.type}
        id={"select-testcase-type"}
        labelTitle={"Add new or existing case?"}
        onClick = {() => {
            isLoading = true;
            if(form.fields.type === "existing"){
                showTestCases = true;
                showNormalForm = false;
            } else{
                showTestCases = false;
                showNormalForm = true;
            }
            isLoading = false;
        }}
    />
    {#if isLoading}
        <LoadingCompnent />
    {:else if showTestCases}
        <ListAllTestSuiteTestCases 
            projectID={form.fields.project_id}
            section={section}
            testSuite={testSuite}
            on:message={
                (event) => {
                    dispatch('message', {
                        obj: event.detail.obj
                    });
                    showTestCases = false;
                    showNormalForm = false;
                }
            }
        />
    {:else if showNormalForm}
        <Input 
            bind:value={form.fields.title} 
            id={"test-case-title-title"} 
            title={"title"} 
            type={"text"}
        />
        <TextArea
            bind:value={form.fields.description}
            title="Description"
        />
        <TextArea
            bind:value={form.fields.test_steps}
            title="Test Steps"
        />
        <TextArea
            bind:value={form.fields.expected_result}
            title="Expected Result"
        />
        {#if projectRequirements && projectRequirements.length > 0}
            <AreaSelect
                objects={projectRequirements}
                bind:value={form.fields.requirement}
                id={"select-testcase-requirement"}
                labelTitle={"Verify requirement"}
            />
        {/if}

        <AddNewTestCase 
            testSuite={testSuite} 
            section={section} 
            testCases={section.test_cases}
            disabled={!validateFields(form.fields)}
            text={"POST"}
            onClick={async () => {
                form.fields.section_id = section.id
                const tccase = await postNewTestCase(form.fields)
                dispatch('message', {
                    obj: tccase
                });
                return claerFields(form.fields)
            }}
        />
    {/if}
</div>