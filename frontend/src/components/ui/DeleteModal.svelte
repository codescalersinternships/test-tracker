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
            if (obj.id) {
                await axios.delete(`${onRequest}/${obj.id}/`, config)
            } else if (obj.title){
                await axios.delete(`${onRequest}/${obj.title}/`, config) // We somtimes want to make request on object has no id
            }
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
                        <h5>You are about to delete <strong class="text-danger">{obj.title}</strong>!!</h5>
                    {:else if obj.email}
                        <h5>You are about to delete <strong class="text-danger">{obj.email}</strong>!!</h5>
                    {/if}
                {/if}
                <span class="text-danger">* </span>Please note that this action cannot be undone.
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