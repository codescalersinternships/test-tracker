<script>
    export let title, value;
</script>


<div class="form-group p-2 mb-2">
    <strong>
        <label for="content-body">{title}</label>
    </strong>
    <textarea bind:value={value} class="form-control mt-2"></textarea>
</div>