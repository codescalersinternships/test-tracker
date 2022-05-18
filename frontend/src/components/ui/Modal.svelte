<script>
    export let message;

    function closeModal() {
        document.querySelector('.modal').style.display = 'none'
    }
</script>

<main>
    <section>
        <!-- Modal -->
        <div class="modal fade top show" id="exampleFrameModal1" tabindex="-1" 
            aria-labelledby="exampleFrameModal1" style="display: none;" aria-modal="true" role="dialog">
            <div class="modal-dialog modal-frame modal-top">
            <div class="modal-content rounded-0">
                <div class="modal-body py-1">
                    <div class="d-flex justify-content-center align-items-center my-3">
                        <p class="pt-3 mx-4">
                            {message}
                        </p>
                        <button type="button" class="btn-close" 
                            aria-label="Close" on:click={closeModal}
                            style="position: absolute;right: 10px;top: 10px;"
                            >
                        </button>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </section>
</main>