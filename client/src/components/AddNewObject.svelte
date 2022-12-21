<script>
    import { createEventDispatcher } from 'svelte';
    import NavBarDropdown from './ui/NavBarDropdown.svelte'
    import CreateNewObjModal from './ui/CreateNewObjModal.svelte'
    import { formFields } from "../healpers/fields"

    let data;
    let fields = formFields();
    const dispatch = createEventDispatcher();

    function createNewObj(key) {
        data = fields[key];
        data.showPostModal = true;
        data.obj = key;
    };
</script>

<div class="d-flex align-items-center">
    <NavBarDropdown>
        <span slot="dropdown-toggle" 
            class="user_photo_nav add-obj">
            <i class="fas fa-plus"></i>
        </span>
        <span slot="dropdown-li">
            {#each Object.entries(fields) as [key, value]}
                <li>
                    <button class="dropdown-item text-primary plus-color primary-hover"
                        on:click={() => createNewObj(key)}>
                        {value.message}
                    </button>
                </li>
            {/each}
        </span>
    </NavBarDropdown>
    {#if data}
        <CreateNewObjModal 
            data={data} 
            current={data.obj} 
            on:message={(event) => {
                dispatch('message', {
                    obj: event.detail.obj,
                });
            }}
        />
    {/if}
</div>