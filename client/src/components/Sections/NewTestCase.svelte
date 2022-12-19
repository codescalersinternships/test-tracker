<script>
    import TextArea from "../ui/TextArea.svelte";
    import Input from "../ui/Input.svelte";
    import AreaSelect from "../ui/AreaSelect.svelte";
    import { onMount } from "svelte";
    import { loadProjectRequirementsBasedOnProjectID } from "../../healpers/api"
    import ListAllTestSuiteTestCases from "./ListAllTestSuiteTestCases.svelte";
    import LoadingCompnent from "../ui/LoodingSpiner.svelte"
    export let fields;

    let projectRequirements;
    let showTestCases = false;
    let showNormalForm = true;
    let isLoading = false;

    const types = [
        {id: "new", title: "New"},
        {id: "existing", title: "Existing"}   
    ]

    onMount(async () => {
        projectRequirements = await loadProjectRequirementsBasedOnProjectID(
            fields.project_id
        );
    });

</script>


<div class="card new-test-case">
    <AreaSelect
        objects={types}
        bind:value={fields.type}
        id={"select-testcase-type"}
        labelTitle={"Add new or existing case?"}
        onClick = {() => {
            isLoading = true;
            if(fields.type === "existing"){
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
        <ListAllTestSuiteTestCases />
    {:else if showNormalForm}
        <Input 
            bind:value={fields.title} 
            id={"test-case-title-title"} 
            title={"title"} 
            type={"text"}
        />
        <TextArea
            bind:value={fields.description}
            title="Description"
        />
        <TextArea
            bind:value={fields.test_steps}
            title="Test Steps"
        />
        <TextArea
            bind:value={fields.expected_result}
            title="Expected Result"
        />
        {#if projectRequirements && projectRequirements.length > 0}
            <AreaSelect
                objects={projectRequirements}
                bind:value={fields.requirement}
                id={"select-testcase-requirement"}
                labelTitle={"Verify requirement"}
            />
        {/if}
    {/if}
</div>