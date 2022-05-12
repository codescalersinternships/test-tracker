<script>
    export let Class = "primary"
    export let Function = null
    export let text = "Submit" 
</script>

<div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
    <button type="button" class="btn btn-{Class} btn-lg" on:click={Function}>{text}</button>
</div>