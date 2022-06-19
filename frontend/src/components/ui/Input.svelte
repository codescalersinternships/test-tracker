<script>
    export let value;
</script>

<div class="form-group p-2 mb-2">
    <label for="content-title">Title</label>
    <input bind:value={value} type="text" class="form-control" id="content-title">
</div>