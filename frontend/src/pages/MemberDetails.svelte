<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    export let user;

    let member;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        var path = window.location.pathname;
        var memberID = path.split("/")[2];
        try {
            const response = await axios.get(`members/${memberID}/`, config);
            member = response.data.data;
        } catch (err) {
            if (err.response.status === 404) {
                window.location.href = "/not-found";
            }
        }
    });

    function openDeleteModal() {
        showDeleteModal = true;
    }
</script>

<svelte:head>
    <title>Test-Tracker | Member Detail</title>
</svelte:head>

<section>
    {#if user && member}
        <NavBar {user} />
        <div class="container pb-5">
            <div class="pt-3 pb-2">
                <p class="h4">
                    About <strong class="h4">{member.full_name}</strong>
                </p>
            </div>
            {#if user.permission === "admin"}
                <div class="col-4">
                    <button
                        type="button"
                        class="btn btn-danger text-white text-decoration-none"
                        on:click={openDeleteModal}
                    >
                        Delete
                    </button>
                </div>
            {/if}
            <div class="card mt-4 p-4">
                <div class="pt-4">
                    <p class="h5 text-muted">Personal Information</p>
                    <hr />
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th scope="row">Full Name</th>
                                <td class="text-dark">{member.full_name}</td>
                                <th scope="row">Email</th>
                                <td class="text-dark">{member.email}</td>
                            </tr>
                            <tr>
                                <th scope="row">Phone Number</th>
                                {#if member.phone.length === 0}
                                    <td class="text-muted">Not set yet</td>
                                {:else}
                                    <td class="text-dark">{member.phone}</td>
                                {/if}
                                <th scope="row">Joined date</th>
                                <td class="text-dark">{member.created}</td>
                            </tr>
                            <tr>
                                <th scope="row">Permission</th>
                                {#if member.permission == "full_access"}
                                    <td class="text-dark">Full Access</td>
                                {:else}
                                    <td class="text-dark">Admin</td>
                                {/if}
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            {#if member.last_project_working_on}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <p class="h5 text-muted">Last Project Worked on</p>
                        <hr />
                        <table class="table table-borderless">
                            <tbody>
                                <tr>
                                    <th scope="row">Name</th>
                                    <td class="text-primary">
                                        <a
                                            href="/projects/{member
                                                .last_project_working_on.id}"
                                        >
                                            {member.last_project_working_on.title.slice(
                                                0,
                                                50
                                            )}
                                        </a>
                                    </td>
                                    <th scope="row">Updated date</th>
                                    <td class="text-dark"
                                        >{member.last_project_working_on
                                            .modified}</td
                                    >
                                </tr>
                                <tr>
                                    <th scope="row">Pinding tasks</th>
                                    {#if member.incomplete_test_runs_assigned_to_you}
                                        <td class="text-primary"
                                            >{member.incomplete_test_runs_assigned_to_you}</td
                                        >
                                    {:else}
                                        <td class="text-muted"
                                            >There are no pinding tasks.</td
                                        >
                                    {/if}
                                    <th scope="row">Created date</th>
                                    <td class="text-dark"
                                        >{member.last_project_working_on
                                            .created}</td
                                    >
                                </tr>
                            </tbody>
                        </table>
                        <strong class="pl-3 text-muted">Team</strong>
                        <br />
                        <hr />
                        <div class="row">
                            {#if member.last_project_working_on.teams.length === 0}
                                <div class="col-6 text-muted">
                                    There are no teams yet, only you.
                                </div>
                            {:else}
                                {#each member.last_project_working_on.teams as person}
                                    <div class="col-2">
                                        <span class="ml-3">
                                            <a
                                                class="text-primary"
                                                href="/members/{person.id}"
                                                >@{person.first_name}</a
                                            >
                                        </span>
                                    </div>
                                {/each}
                            {/if}
                        </div>
                    </div>
                </div>
            {/if}
            {#if member.last_tests_assigned}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <p class="h5 text-muted">Last Test Run Assigned</p>
                        <hr />
                        <table class="table table-borderless">
                            <tbody>
                                <tr>
                                    <th scope="row">Name</th>
                                    <td
                                        ><a
                                            href="/projects/{member
                                                .last_tests_assigned
                                                .project_id}/runs/{member
                                                .last_tests_assigned.id}"
                                            class="text-primary"
                                            >{member.last_tests_assigned.title.slice(
                                                0,
                                                50
                                            )}</a
                                        ></td
                                    >
                                    <th scope="row">Date</th>
                                    <td class="text-primary"
                                        >{member.last_tests_assigned
                                            .created}</td
                                    >
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
    <DeleteModal
        bind:showDeleteModal
        obj={member}
        onRequest="/members/"
        {config}
        redirect="/members/"
    />
</section>
