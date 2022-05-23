<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'
    import NavBar from "../components/NavBar.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"
    export let user;

    let member;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };
    
    onMount(async () => {
        var path = window.location.pathname;
        var memberID = path.split("/")[2];
        try {
            const response = await axios.get(`members/${memberID}/`, config)
            member = response.data.data
        }catch(err) {
            if(err.response.status === 404){
                window.location.href = '/not-found'
            }
        }
    });

    function openModal(member) {
        document.querySelector('.modal').style.display = 'block'
    }

</script>

<svelte:head>
    <title>Test-Tracker | Member Detail</title>
</svelte:head>

<section>
    {#if user && member}
        <NavBar user={user}/>
        <div class="container pb-5">
            <div class="pt-5">
                <p class="h4">About <strong class="h4">{member.full_name}</strong></p>
            </div>
            {#if user.permission === "admin"}
                <div class="col-4 pt-5">
                    <button type="button" class="btn btn-danger text-white text-decoration-none" 
                        on:click={openModal}>
                        Delete
                    </button>
                </div>
            {/if}
            <div class="card mt-4 p-4">
                <div class="pt-4">
                    <p class="h5 text-muted">Personal Information</p>
                    <hr>
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th scope="row">Full Name</th>
                                <td class="text-primary">{member.full_name}</td>
                                <th scope="row">Email</th>
                                <td class="text-primary">{member.email}</td>
                            </tr>
                            <tr>
                                <th scope="row">Phone Number</th>
                                {#if member.phone.length === 0}
                                    <td class="text-muted">Not set yet</td>
                                {:else}
                                    <td class="text-primary">{member.phone}</td>
                                {/if}
                                <th scope="row">Joined date</th>
                                <td class="text-primary">{member.created}</td>
                            </tr>
                            <tr>
                                <th scope="row">Permission</th>
                                {#if member.permission == "full_access"}
                                    <td class="text-primary">Full Access</td>
                                {:else}
                                    <td class="text-primary">Admin</td>
                                {/if}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card mt-4 p-4">
                <div class="pt-4">
                    <p class="h5 text-muted">Last Project Worked on</p>
                    <hr>
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th scope="row">Name</th>
                                <td class="text-primary">{member.last_project_working_on.title.slice(0, 50)}</td>
                                <th scope="row">Updated date</th>
                                <td class="text-primary">{member.last_project_working_on.modified}</td>
                            </tr>
                            <tr>
                                <th scope="row">Pinding tasks</th>
                                {#if member.incomplete_test_runs_assigned_to_you}
                                    <td class="text-primary">{member.incomplete_test_runs_assigned_to_you}</td>
                                {:else}
                                    <td class="text-muted">There are no pinding tasks.</td>
                                {/if}
                                <th scope="row">Created date</th>
                                <td class="text-primary">{member.last_project_working_on.created}</td>
                            </tr>
                        </tbody>
                    </table>
                    <strong class="pl-3 text-muted">Team</strong>
                    <br/><hr>
                    <div class="row">
                        {#if member.last_project_working_on.teams.length === 0 }
                            <div class="col-6 text-muted">There are no teams yet, only you.</div>
                        {:else}
                            {#each member.last_project_working_on.teams as person }
                            <div class="col-2">
                                <span class="ml-3">
                                    <a class="text-primary" href="/members/{person.id}">@{person.first_name}</a>
                                </span>
                            </div>
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>
            {#if member.last_tests_assigned}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <p class="h5 text-muted">Last Tests Assigned</p>
                        <hr>
                        <table class="table table-borderless">
                            <tbody>
                                <tr>
                                    <th scope="row">Name</th>
                                    <td class="text-primary">{member.last_tests_assigned.title.slice(0, 50)}</td>
                                    <th scope="row">Date</th>
                                    <td class="text-primary">{member.last_tests_assigned.created}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Description</th>
                                    <div class="card">
                                        {member.last_tests_assigned.description}
                                    </div>
                                </tr>
                                <tr>
                                    <th scope="row">Steps</th>
                                    <div class="card">
                                        {member.last_tests_assigned.test_steps}
                                    </div>
                                </tr>
                                <tr>
                                    <th scope="row">Expected Result</th>
                                    <div class="card">
                                        {member.last_tests_assigned.expected_result}
                                    </div>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
    <DeleteModal
        obj={member}
        onRequest='/members'
        config={config}
        redirect='/members'
    />
</section>
