<script>
    export let updateFunctionOnClick, title, body;

    function contentAreaModalAction() {
        // Close and open the modal window
        if (document.querySelector('.update-content-modal').style.display === 'block') {
            document.querySelector('.update-content-modal').style.display = 'none'
        } else {
            document.querySelector('.update-content-modal').style.display = 'block'
        }
    }


</script>

<div class="modal update-content-modal" tabindex="-1" style="display: none;">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                <div class="modal-header">
                    <h5>Add new content area</h5>
                </div>
                <form>
                    <div class="form-group p-2">
                        <label for="content-title">Title</label>
                        <input bind:value="{title}" type="text" class="form-control" id="content-title">
                    </div>
                    <div class="form-group p-2">
                        <label for="content-body">Content</label>
                        <textarea bind:value="{body}" class="form-control" id="content-body"></textarea>
                    </div>
                </form>
                <strong>
                    <small>
                        <span class="text-danger">* Please note that,</span> if you try to add a new content area with an exact content area title that means you make an update on it,
                        not post a new one
                    </small>
                </strong>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" 
                        on:click={contentAreaModalAction}>Close</button>
                    <button class="btn btn-success" data-mdb-dismiss="modal" 
                        on:click={updateFunctionOnClick({title}, {body})}>Update</button>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    textarea {
        height: 150px; 
        max-height: 150px
    }
</style>