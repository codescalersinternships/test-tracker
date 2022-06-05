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
        try {
            if (member) {
                const response = await axios.put(`project/${projectID}/members/${member}/`, [], config);
                dispatch("message", {
                    members: response.data.data,
                });
                showAddMemberModal = false;
            }else{
                alert("Please select a member");
            }
        } catch (err) {
            if (err.response.status == 400){
                alert("Member already in project");
            }
        }
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
                    {#if members}
                        <select
                            bind:value={member}
                            class="form-select"
                            aria-label="select-status"
                            id="select-status"
                        >
                            <option selected />
                            {#each members as member}
                                <option value={member.id}>{member.first_name} {member.last_name}</option>
                            {/each}
                        </select>
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
                <button
                    type="button"
                    class="btn btn-success text-white text-decoration-none"
                    on:click={addMember}
                >
                    Add Member
                </button>
            </div>
        </div>
    </div>
</div>