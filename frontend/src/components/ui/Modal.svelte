<script>
    export let textArea = false;

    function contentAreaModalAction() {
        if (document.querySelector('.custom-modal').style.display === 'block') {
            document.querySelector('.custom-modal').style.display = 'none'
        } else {
            document.querySelector('.custom-modal').style.display = 'block'
        }
    }


</script>

<div class="modal custom-modal" tabindex="-1" style="display: none;">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                <form>
                    <div class="form-group p-2">
                      <label for="content-title">Title</label>
                      <input type="text" class="form-control" id="content-title">
                    </div>
                    {#if textArea}
                        <div class="form-group p-2">
                        <label for="content-body">Content</label>
                        <textarea class="form-control" id="content-body" style="height: 150px; max-height: 150px"></textarea>
                        </div>
                    {/if}
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={contentAreaModalAction}>Close</button>
                <button type="button" class="btn btn-success" data-mdb-dismiss="modal" on:click={addNewContentArea}>Add</button>
            </div>
        </div>
    </div>
</div>