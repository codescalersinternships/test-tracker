<script>
    function homePage() {
        window.location.href = '/'
    }

</script>

<svelte:head>
 <title>Not Found</title>
</svelte:head>

<section>
    <div class="page-wrap d-flex flex-row align-items-center">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-12 text-center">
                    <span class="display-1 d-block">404</span>
                    <div class="mb-4 lead">The page you are looking for was not found.</div>
                    <button type="button" class="btn btn-primary " 
                        on:click={homePage}>
                        Back to Home
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
