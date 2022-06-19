<script>
    export let message, showAlert, _class;
</script>

<section>
    <div class="alert alert-{_class} text-dark text-center"
        style={`display: ${showAlert ? "block" : "none"};`}
        >
        <p class="m-0">{message}</p>
    </div>
</section>


