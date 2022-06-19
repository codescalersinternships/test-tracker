<script>
    export let title, value;
</script>


<div class="form-group p-2 mb-2">
    <label for="content-body">{title}</label>
    <textarea bind:value={value} class="form-control"></textarea>
</div>