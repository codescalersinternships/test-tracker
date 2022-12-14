<script>
    import NewSection from "./NewSection.svelte"
    import Loadingbtn from "../ui/Loadingbtn.svelte"
    let isLoading = false;
    let clickedButton;
    let value = false;

    const addNewSection = () => {
        isLoading = true;
        value = clickedButton.classList.toggle("new-section-clicked");
        isLoading = false;
    }
</script>



{#if value}
    <div class="clicked">
        <NewSection bind:value />
    </div>
{:else}
    <div class="d-flex align-items-center justify-content-end" bind:this={clickedButton}>
        <button
            disabled={false}
            class="btn new-section-button" 
            on:click={addNewSection}>
            {#if isLoading}
                <Loadingbtn />
            {:else}
                Add new section
            {/if}
        </button>
    </div>
{/if}
