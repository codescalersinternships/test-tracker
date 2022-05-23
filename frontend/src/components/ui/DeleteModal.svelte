<script>
    import { createEventDispatcher } from 'svelte';
    import axios from '../../healpers/axios'
    
    export let onRequest; // [request] for the endpoint
    export let obj; // [obj] is the object to be deleted
    export let config; // [config] is the config for the request
    export let redirect = null; // [redirect] is the url to redirect to after deleting

    const dispatch = createEventDispatcher();
    function closeModal() {document.querySelector('.delete-modal').style.display = 'none'}
    
    async function deleteObj() {
        dispatch('message', {
			obj: obj
		});

        try {
            await axios.delete(`${onRequest}/${obj.id}/`, config)
            closeModal()
            if (redirect){
                window.location.href = redirect
            }
        } catch (err) {
            console.log(err);
        }
    }

</script>

<div class="modal delete-modal" tabindex="-1" style="display: none;">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-body">
                {#if obj}
                    {#if obj.title}
                        <h5>Are you sure you want to delete {obj.title}?</h5>
                    {:else if obj.email}
                        <h5>Are you sure you want to delete {obj.email}?</h5>
                    {:else}
                        <h5>Are you sure you want to delete this?</h5>
                    {/if}
                {/if}
                Please note that this action cannot be undone.
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={closeModal}>Close</button>
                <button type="button" class="btn btn-danger text-white text-decoration-none" 
                    on:click={deleteObj}>
                    Delete
                </button>
            </div>
        </div>
    </div>
</div>