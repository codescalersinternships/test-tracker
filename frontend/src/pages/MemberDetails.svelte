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
            <div class="row pt-3 pb-2">
                <div class="col-11">
                    <p class="h4 mb-2">
                        About | <strong class="h4 text-primary">{member.full_name}</strong>
                    </p>
                </div>
                {#if user.permission === "admin"}
                    <div class="col-1">
                        <button
                            type="button"
                            class="btn plus-background text-white text-decoration-none"
                            on:click={openDeleteModal}
                            >
                            Delete
                        </button>
                    </div>
                {/if}
            </div>
            <div class="card mt-4 p-4">
                <div class="pt-4">
                    <p class="h5 text-muted">Personal Information</p>
                    <hr />
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th scope="row" class="text-muted">Full Name</th>
                                <td class="text-primary">{member.full_name}</td>
                                <th scope="row" class="text-muted">Email</th>
                                <td class="text-primary">{member.email}</td>
                            </tr>
                            <tr>
                                <th scope="row" class="text-muted">Phone Number</th>
                                {#if member.phone.length === 0}
                                    <td class="text-muted">Not set yet</td>
                                {:else}
                                    <td class="text-primary">{member.phone}</td>
                                {/if}
                                <th scope="row" class="text-muted">Joined date</th>
                                <td class="text-primary">{member.created}</td>
                            </tr>
                            <tr>
                                <th scope="row" class="text-muted">Permission</th>
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
            {#if member.last_project_working_on}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <p class="h5 text-muted">Last Project Worked on</p>
                        <hr />
                        <table class="table table-borderless">
                            <tbody>
                                <tr>
                                    <th scope="row" class="text-muted">Name</th>
                                    <td class="text-primary">
                                        <a class="text-primary"
                                            href="/projects/{member
                                                .last_project_working_on.id}"
                                        >
                                            {member.last_project_working_on.title.slice(
                                                0,
                                                50
                                            )}
                                        </a>
                                    </td>
                                    <th scope="row" class="text-muted">Updated date</th>
                                    <td class="text-primary"
                                        >{member.last_project_working_on
                                            .modified}</td
                                    >
                                </tr>
                                <tr>
                                    <th scope="row" class="text-muted">Pinding tasks</th>
                                    {#if member.incomplete_test_runs_assigned_to_you}
                                        <td class="text-primary"
                                            >{member.incomplete_test_runs_assigned_to_you}</td
                                        >
                                    {:else}
                                        <td class="text-muted"
                                            >There are no pinding tasks.</td
                                        >
                                    {/if}
                                    <th scope="row" class="text-muted">Created date</th>
                                    <td class="text-primary"
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
                                <div class="col-12 text-muted">
                                    <p class="text-center">
                                        There are no teams yet, only you.
                                    </p>
                                </div>
                            {:else}
                                {#each member.last_project_working_on.teams as person}
                                    {#if person.id != member.id}
                                        <div class="col-2">
                                            <span class="ml-3">
                                                <a
                                                    class="link-color"
                                                    href="/members/{person.id}"
                                                    >@{person.first_name}</a
                                                >
                                            </span>
                                        </div>
                                    {:else}
                                        <div class="col-12 text-muted">
                                            <p class="text-center">
                                                There are no teams yet, only you.
                                            </p>
                                        </div>
                                    {/if}
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
                                    <th scope="row" class="text-muted">Name</th>
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
                                    <th scope="row" class="text-muted">Date</th>
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
        onRequest="/members"
        redirect="/members/"
    />
</section>
