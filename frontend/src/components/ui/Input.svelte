<script>
    export let value;
</script>

<div class="form-group p-2 mb-2">
    <strong>
        <label for="content-title">Title</label>
    </strong>
    <input bind:value={value} type="text" class="form-control mt-2" id="content-title">
</div>