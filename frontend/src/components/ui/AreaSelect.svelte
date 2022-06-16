<script>
    import { createEventDispatcher } from 'svelte';
    export let objects, id, labelTitle, value;
    const dispatch = createEventDispatcher();
</script>

<div class="form-group p-2 mb-3">
    <label for={id}>{labelTitle}</label>
    <select
        class="form-select"
        aria-label={id}
        id={id}
        bind:value={value}
        >
        {#each objects as object }
            <option value={object.id}>{object.title}</option>
        {/each}
    </select>
</div>