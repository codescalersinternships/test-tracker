<script>
    export let group, id, value, title;
</script>


<div class="form-check">
    <input 
        class="form-check-input" 
        bind:group={group} 
        value={value} type="radio" 
        id={id}
    />
    <label 
        class="form-check-label" 
        for={id}>
        {title}
    </label>
</div>