<script>
    export let Class = "primary"
    export let Function = null
    export let text = "Submit" 
</script>

<button type="button" class={Class} on:click={Function}>{text}</button>