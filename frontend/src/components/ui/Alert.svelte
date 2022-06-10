<script>
    export let message, showAlert, _class;
</script>

<section>
    <div class="alert alert-{_class} text-dark"
        style={`display: ${showAlert ? "block" : "none"};`}
        >
        <h4 class="alert-heading">Like Test Tracker Said!</h4>
        <p>{message}</p>
    </div>
</section>


