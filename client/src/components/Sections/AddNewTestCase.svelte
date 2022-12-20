<script>
    import Loadingbtn from "../ui/Loadingbtn.svelte";
    import { createEventDispatcher } from 'svelte';
    import NewTestCase from "./NewTestCase.svelte";

    export let section;
    export let testSuite;
    export let onClick;
    export let disabled;
    export let text;

    let isOpined = false;
    let openModal = false;
    let isLoading = false;

    const dispatch = createEventDispatcher();

    const addNewTestCase = () => {
        isLoading = true;
        isOpined = true;
        openModal = true;
        isLoading = false;
    };
    
</script>


{#if openModal}
    <NewTestCase
        section={section}
        testSuite={testSuite}
        on:message={(event) => {
            dispatch('message', {
                obj: event.detail.obj,
            });
            openModal = false;
        }}
    />
{/if}

{#if !isOpined}
    <div class="d-flex mt-4 align-items-center justify-content-end">
        <button
            disabled={disabled}
            class="btn new-section-button" 
            on:click|preventDefault={async () => {
                isLoading = true;
                isOpined = true;
                if(onClick){
                    await onClick()
                } else {
                    addNewTestCase()
                }
                isLoading = false;
                isOpined = false;
            }}>
            {#if isLoading}
                <Loadingbtn />
            {:else}
                {text}
            {/if}
        </button>
    </div>
{/if}
