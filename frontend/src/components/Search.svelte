<script>
    import Button from "./ui/Button.svelte";
    
    export let title;
    export let searchFunction;
</script>



<section>
    <div class="pt-4">
        <p>
            {title}
        </p>
        <div class="input-group">
            <input id="search-id" type="search" class="form-control rounded" placeholder="Search"
            aria-label="Search" aria-describedby="search-addon" />
            <Button Class="btn btn-outline-primary" Function={searchFunction} text="Search" />
        </div>
    </div>
</section>