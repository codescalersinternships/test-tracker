<script>    
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
            <button type="button" class="btn btn-outline-primary" 
                on:click={searchFunction}>
                Search
            </button>
        </div>
    </div>
</section>