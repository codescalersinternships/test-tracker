<script>
    import { deleteSection } from "../../healpers/api";
    import { createEventDispatcher } from 'svelte';
    import Input from "../ui/Input.svelte";

    export let openDeleteModal = false;
    export let section = false;

    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let disabled = true;
    let value;

    const dispatch = createEventDispatcher();

    const checkToDelete = () => {
        if(value === section.title){
            disabled = false;
        };
    };

    $: value, checkToDelete();
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
    style={`display: ${openDeleteModal ? "block" : "none"};`}
>
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <span>
                    You are about to delete section 
                    <strong class="text-primary">
                        {section.title}
                    </strong>
                    so unexpected bad things will happen if you don’t read this!
                </span>
            </div>
            <div class="modal-body">
                <div class="alert alert-warning">
                    This action cannot be undone. <strong>This will permanently delete all this section and its test cases</strong>, the test cases will be without any section,
                    <strong>but you can link them to another section in the future</strong>.
                </div>
                <p class="p-0 m-0">Please type <strong class="text-primary">
                    {section.title}
                </strong> to confirm.</p>
                <Input bind:value title={false} type={"text"} id={"delete-section"}/>
            </div>
            <div class="modal-footer">
                <button
                    type="button"
                    class="btn btn-primary"
                    data-mdb-dismiss="modal"
                    on:click={() => (openDeleteModal = false)}>
                Close
                </button>
                <button
                    disabled={disabled}
                    type="button"
                    class="btn btn-danger"
                    data-mdb-dismiss="modal"
                    on:click={() => {
                        deleteSection(projectID, section.id);
                        dispatch('message', {
                            deletedSection: section,
                        });
                        openDeleteModal = false;
                    }}>
                Delete
                </button>
            </div>
        </div>
    </div>
</div>
