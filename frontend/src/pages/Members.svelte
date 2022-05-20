<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";

    export let user;

    let members, membersCopy, memberEmail;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        try {
            const response = await axios.get('/members/all/', config)
            members = await response.data.data
            membersCopy = members
        } catch (err) {
            if (err.response.status === 403){
                window.location.href = '/not-found'
            }
        }
    });


    async function searchMembers(params) {
        var inputValue = document.getElementById('search-id').value,
            endPoint = `members/search/${inputValue}/`;
        if (inputValue){
            const result = await axios.get(endPoint, config)
            members = result.data.data 
        } else{
            members = membersCopy
        }
    }

    async function deleteMember(email){
        try {
            await axios.delete(`/members/${email}/`, config)
            closeModal()
            window.location.reload()
        } catch (err) {
            console.log(err);
        }
    }

    function openModal(email) {
        memberEmail = email;
        document.querySelector('.modal').style.display = 'block'
    }

    function closeModal() {document.querySelector('.modal').style.display = 'none'}

</script>

<svelte:head>
    <title>Test-Tracker | Members</title>
</svelte:head>

<section>
    {#if user}
        {#if members}
            <NavBar user={user}/>
            <div class="container">
                <div class="pt-5">
                    <strong class="h4">All Members</strong>
                    There are <strong>{members.length}</strong> {user.total_projects === 1 ? 'member' : 'members'} registered
                </div>
                <Search title="Search Members:" searchFunction={searchMembers}/>
                <div class="pt-5">
                    <div class="row">
                        {#if members.length > 0}
                            {#each members as member}
                                <div class="col-lg-4 col-md-6 col-sm-12 col-xs-12">
                                    <div class="card mt-4" style="width: 18rem;">
                                        <div class="card-body">
                                            <h5 class="card-title">{member.full_name}</h5>
                                            {#if member.permission === "full_access"}
                                                <h6 class="card-subtitle mb-2 text-muted">Full access</h6>
                                            {:else if member.permission === "admin_access"}
                                                <h6 class="card-subtitle mb-2 text-muted">Admin</h6>
                                            {/if}
                                            {#if member.last_project_working_on.name.length > 0}
                                                <p class="card-text">Working on: <span class="text-primary">
                                                    {member.last_project_working_on.name}
                                                </span></p>
                                            {:else}
                                                <p class="card-text">Working on: <span class="text-primary">
                                                    Not working on any project
                                                </span></p>
                                            {/if}
                                            <p class="card-text text-muted">Joined on: {member.created}</p>
                                            <a href={`/members/${member.id}`} class="btn btn-primary text-white text-decoration-none">View</a>
                                            <button type="button" class="btn btn-danger text-white text-decoration-none" 
                                                on:click={openModal(member.email)}>
                                                Delete
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            {/each}
                        {:else}
                            <div class="col-12 pt-5">
                                <p class="text-muted">
                                    -- There are no members
                                </p>
                            </div>
                        {/if}
                    </div>
                </div>
            </div>
            <!-- Modal -->
            <div class="modal" tabindex="-1" style="display: none;">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">You are about to delete this member.</h5>
                        </div>
                        <div class="modal-body">
                            <p>Please note that <strong>{memberEmail}</strong> cannot access the whole Test-Tracker after you confirm.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" data-mdb-dismiss="modal" on:click={closeModal}>Close</button>
                            <button type="button" class="btn btn-danger text-white text-decoration-none" 
                                on:click={deleteMember(memberEmail)}>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    {:else}
        <LoodingSpiner />
    {/if}
</section>