<script>
    export let showUpdateModal = false;
    export let updateData;
    
    function updateObj() {
        console.log('updateObj');
    }
</script>

<div
    class="modal update-modal"
    tabindex="-1"
    style={`display: ${showUpdateModal ? "block" : "none"};`}
>    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body p-4">
                {#if updateData}
                    <div class="modal-header">
                        <h5>Update {updateData.updateFieldTitle}</h5>
                    </div>
                    <form>
                        <div class="form-group p-2">
                            <label for="content-title">Title</label>
                            <input bind:value="{updateData.title}" type="text" class="form-control" id="content-title">
                        </div>
                        <slot></slot>
                        <div class="form-group p-2">
                            <label for="content-body">Content</label>
                            <textarea bind:value="{updateData.body}" class="form-control" id="content-body"></textarea>
                        </div>
                    </form>
                {/if}
                <!-- <strong>
                    <small>
                        <span class="text-danger">* Please note that,</span> if you try to add a new content area with an exact content area title that means you make an update on it,
                        not post a new one
                    </small>
                </strong> -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" 
                        on:click={() => (showUpdateModal = false)}>Close</button>
                    <button class="btn btn-success" data-mdb-dismiss="modal" 
                        on:click={updateObj}>Update</button>
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