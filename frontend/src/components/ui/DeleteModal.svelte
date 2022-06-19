<script>
    import { createEventDispatcher } from "svelte";
    import axios from "../../healpers/axios";

    export let onRequest = null; // [request] for the endpoint
    export let obj = null; // [obj] is the object to be deleted
    export let redirect = null; // [redirect] is the url to redirect to after deleting
    export let showDeleteModal = false;

    const dispatch = createEventDispatcher();

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    async function deleteObj(e) {
        const node = e.currentTarget;
        node.disabled = true;

        dispatch("message", {
            obj: obj,
        });

        try {
            if (obj.id) {
                await axios.delete(`${onRequest}/${obj.id}/`, config);
            } else if (obj.title) {
                await axios.delete(`${onRequest}/${obj.title}/`, config); // We somtimes want to make request on object has no id
            }
            showDeleteModal = false;
            // closeModal()
            if (redirect) {
                window.location.href = redirect;
            }
        } catch (err) {
            console.log(err);
        } finally {
            node.disabled = false;
        }
    }
</script>

<svelte:head>
    <style>
        .alert_delete {
            font-size: 17px;
            color: #ec1b1be8;
        }
    </style>
</svelte:head>

<div
    class="modal delete-modal"
    tabindex="-1"
    style={`display: ${showDeleteModal ? "block" : "none"};`}
>
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body">
                {#if obj}
                    {#if obj.title}
                        <h5>
                            You are about to delete <strong class="alert_delete"
                                >" {obj.title} "
                            </strong>!!
                        </h5>
                    {:else if obj.email}
                        <h5>
                            You are about to delete <strong class="alert_delete"
                                >" {obj.email} "
                            </strong>!!
                        </h5>
                    {/if}
                {/if}
                <span class="text-danger">* </span>Please note that this action
                cannot be undone.
            </div>
            <div class="modal-footer">
                <button
                    type="button"
                    class="btn btn-primary"
                    data-mdb-dismiss="modal"
                    on:click={() => (showDeleteModal = false)}>Close</button
                >
                <button
                    type="button"
                    class="btn plus-background text-white text-decoration-none"
                    on:click={(e) => deleteObj(e)}
                >
                    Delete
                </button>
            </div>
        </div>
    </div>
</div>
