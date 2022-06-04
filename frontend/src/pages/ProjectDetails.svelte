<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";

    export let user;

    let project, activity;
    let showDeleteModal = false;
    var path = window.location.pathname;
    var projectID = path.split("/")[2];

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        try {
            const response = await axios.get(`project/${projectID}/`, config);
            project = await response.data.data;
            activity = project.activity;
        } catch (err) {
            if (err.response.status === 404 || err.response.status === 403) {
                window.location.href = "/not-found";
            }
        }
    });

    function openDeleteModal() {
        showDeleteModal = true;
    }
</script>

<section>
    {#if user}
        <NavBar projectView="true" {user} />
        {#if project}
            <div class="container mt-4">
                <p class="h4 mb-2">
                    Project overview & activity of
                    <strong class="h4 title">{project.title}</strong>
                </p>
                {#if user.permission === "admin"}
                    <div class="col-4 mt-3">
                        <button
                            type="button"
                            class="btn btn-danger text-white text-decoration-none"
                            on:click={openDeleteModal}
                        >
                            Delete
                        </button>
                        <button
                            type="button"
                            class="btn btn-success text-white text-decoration-none"
                            on:click={openDeleteModal}
                        >
                            Add Member
                        </button>
                    </div>
                {/if}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <div class="col-6">
                            <p class="h5 text-muted">Project Statistics</p>
                        </div>
                        <hr />
                    </div>
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th scope="row">Total test plans</th>
                                <td class="text-primary"
                                    >{project.total_test_plan.length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row">Total Requirements Docs</th>
                                <td class="text-primary"
                                    >{project.total_requirements_docs
                                        .length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row">Total Test Suites</th>
                                <td class="text-primary"
                                    >{project.total_suites.length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row">Total Test Runs</th>
                                <td class="text-primary"
                                    >{project.total_test_runs.length}</td
                                >
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <div class="col-6">
                            <p class="h5 text-muted">Project Team</p>
                        </div>
                        <hr />
                    </div>
                    <div class="row">
                        {#each project.teams as member}
                            <div class="col-2">
                                <a href="/members/{member.id}"
                                    >@{member.first_name}</a
                                >
                            </div>
                        {:else}
                            <p class="text-muted">There are no members.</p>
                        {/each}
                    </div>
                </div>
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <div class="row">
                            <div class="col-6">
                                <p class="h5 text-muted">
                                    Incomplete test runs assigned to you
                                </p>
                            </div>
                            <div class="col-6 text-muted">
                                <p class="h5">
                                    People with the most incomplete test runs
                                </p>
                            </div>
                        </div>
                        <hr />
                        <div class="row">
                            <div class="col-6">
                                <table class="table table-borderless">
                                    {#if project.incomplete_test_runs_assigned_to_you}
                                        <tbody>
                                            <tr>
                                                <th scope="row"
                                                    >{project
                                                        .incomplete_test_runs_assigned_to_you
                                                        .title}</th
                                                >
                                                <td class="text-primary"
                                                    >{project
                                                        .incomplete_test_runs_assigned_to_you
                                                        .created}</td
                                                >
                                            </tr>
                                        </tbody>
                                    {:else}
                                        <tbody>
                                            <tr>
                                                <td class="text-muted"
                                                    >There are no incompleted
                                                    task for you</td
                                                >
                                            </tr>
                                        </tbody>
                                    {/if}
                                </table>
                            </div>
                            <div class="col-6">
                                <table class="table table-borderless">
                                    {#each project.people_with_the_most_incomplete_test_runs as task}
                                        <tbody>
                                            <tr>
                                                <td class="text-primary">
                                                    <strong class="text-dark"
                                                        >TestRun:
                                                    </strong>
                                                    <a
                                                        href="/projects/{projectID}/runs/{task.id}"
                                                        >{task.title}</a
                                                    >
                                                </td>
                                                <td class="text-primary">
                                                    <strong class="text-dark"
                                                        >User:
                                                    </strong>
                                                    <a
                                                        href="/members/{task
                                                            .assigned_user.id}"
                                                        >@{task.assigned_user
                                                            .first_name}</a
                                                    >
                                                </td>
                                            </tr>
                                        </tbody>
                                    {:else}
                                        <tbody>
                                            <tr>
                                                <td class="text-muted"
                                                    >There are no pinding tasks</td
                                                >
                                            </tr>
                                        </tbody>
                                    {/each}
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <ActivityTable {activity} />
            </div>
            <DeleteModal
                bind:showDeleteModal
                onRequest="project"
                obj={project}
                redirect="/projects/"
            />
        {/if}
    {:else}
        <LoodingSpiner />
    {/if}
</section>

<svelte:head>
    <title>Test-Tracker | Project Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
    </style>
</svelte:head>
