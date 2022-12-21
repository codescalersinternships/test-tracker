<script>
    export let value, title, type, id, disabled = false;

    function typeAction(node) {
		node.type = type;
	}
</script>

<div class="form-group p-2 mb-2">
    {#if title}
        <strong>
            <label for={id}>{title}</label>
        </strong>
        <input bind:value use:typeAction disabled={disabled}
            class="form-control mt-2 input" id={id}
        >
    {:else}
        <input bind:value use:typeAction disabled={disabled}
            class="form-control mt-2 input" id={id}
        >
    {/if}
</div>