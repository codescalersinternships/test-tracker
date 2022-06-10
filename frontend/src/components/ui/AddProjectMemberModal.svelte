<script>
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    import axios from "../../healpers/axios";

    export let showAddMemberModal = false;

    const dispatch = createEventDispatcher();

    let members, member;

    var path = window.location.pathname;
    var projectID = path.split("/")[2];

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        try {
            const response = await axios.get(`project/${projectID}/account-members-not-in-project-members/`, config);
            members = response.data.data;
        } catch (err) {
            if (err.response.status === 404) {
                window.location.href = "/not-found";
            }
        }
    })

    async function addMember(){
        await axios.put(`project/${projectID}/members/${member}/`, [], config);
        const indx = members.findIndex((v) => v.id === member);
        dispatch("message", {member:members[indx]});
        members = members;
        members.splice(indx, 1);
        showAddMemberModal = false;
    }

</script>
<div
    class="modal set-project-member-modal"
    tabindex="-1"
    style={`display: ${showAddMemberModal ? "block" : "none"};`}
>
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body">
                <div class="col-12">
                    <div class="col-6 pb-2">
                        <strong>
                            <label for="#select-status">Add New Member</label>
                        </strong>
                    </div>
                    {#if members && members.length > 0}
                        <select
                            bind:value={member}
                            class="form-select"
                            aria-label="select-status"
                            id="select-status"
                        >
                            {#each members as member}
                                <option value={member.id}>{member.first_name} {member.last_name}</option>
                            {/each}
                        </select>
                    {:else}
                        <div class="col-12">
                            <p class="text-center">No members to add.</p>
                        </div>
                    {/if}
                </div>
            </div>
            <div class="modal-footer">
                <button
                    type="button"
                    class="btn btn-primary"
                    data-mdb-dismiss="modal"
                    on:click={() => (showAddMemberModal = false)}>Close</button
                >
                {#if members && members.length > 0}
                    <button
                        type="button"
                        class="btn btn-success text-white text-decoration-none"
                        on:click={addMember}
                    >
                        Add Member
                    </button>
                {/if}
            </div>
        </div>
    </div>
</div>