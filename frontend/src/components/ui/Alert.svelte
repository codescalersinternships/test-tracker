<script>
    export let message;

    function hideAlert() {
        document.querySelector('.alert').style.display = 'none'
    }
</script>

<section>
    <div class="alert alert-danger text-dark" style="display: none;" role="alert">
        <h4 class="alert-heading">Ooops!</h4>
        <p>{message}</p>
        <button type="button" class="btn-close" 
            aria-label="Close" on:click={hideAlert}
            style="position: absolute;right: 10px;top: 10px;"
            >
        </button>
    </div>
</section>


