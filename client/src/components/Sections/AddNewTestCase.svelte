<script>
    import Loadingbtn from "../ui/Loadingbtn.svelte";
    import { createEventDispatcher } from 'svelte';
    import NewTestCase from "./NewTestCase.svelte";
    import { newTestCaseFields } from "../../healpers/fields"

    export let testCases = [];

    let isLoading = false;
    let clickedButton;
    let openModal = false;
    let fields = newTestCaseFields();
    const dispatch = createEventDispatcher();

    const addNewTestCase = async () => {
        isLoading = true;
        openModal = true;
        console.log(fields["test_case"]);
        // response = clickedButton.classList.toggle("new-section-clicked");
        // isLoading = false;
    }
</script>


{#if openModal}
    <NewTestCase 
        fields={fields} 
        on:message={(event) => {
            dispatch('message', {
                obj: event.detail.obj,
            });
        }}
    />
{/if}

<div class="d-flex align-items-center justify-content-end" bind:this={clickedButton}>
    <button
        disabled={false}
        class="btn new-section-button" 
        on:click={addNewTestCase}>
        {#if isLoading}
            <Loadingbtn />
        {:else}
            Add new test case
        {/if}
    </button>
</div>

