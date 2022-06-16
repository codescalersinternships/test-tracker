<script>
    import { createEventDispatcher } from 'svelte';
    export let value = '';
    const dispatch = createEventDispatcher();

</script>


<div class="form-group p-2">
    <label for="content-body">Short Description</label>
    <textarea bind:value={value} class="form-control"></textarea>
</div>