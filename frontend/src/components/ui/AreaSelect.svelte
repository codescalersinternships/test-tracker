<script>
    export let objects, id, labelTitle, value, user=false;
</script>

<div class="form-group p-2 mb-3">
    <strong>
        <label for={id}>{labelTitle}</label>
    </strong>
    <select
        class="form-select mt-2"
        aria-label={id}
        id={id}
        bind:value={value}
        >
        {#each objects as object }
            {#if user}
                <option value={object.id}>{object.full_name}</option>
            {:else}
                <option value={object.id}>{object.title}</option>
            {/if}
        {/each}
    </select>
</div>