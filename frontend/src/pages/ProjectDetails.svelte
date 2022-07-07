<script>
    import { Router, Link } from "svelte-navigator";
    import { onMount } from "svelte";

    import axios from "../healpers/axios";
    
    import NavBar from "../components/NavBar.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import AddProjectMemberModal from "../components/ui/AddProjectMemberModal.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";

    export let user;

    let project, activity, showDeleteModal, showAddMemberModal;
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
    function openAddMemberModal() {
        showAddMemberModal = true;
    }
    async function handleAddMember(event) {
        project.teams = project.teams;
        project.teams.push(event.detail.member);
    }
</script>

<section>
    {#if user}
        <NavBar projectView="true" {user} />
        {#if project}
            <div class="container mt-4">
                {#if user.permission === "admin"}
                    <div class="col-12 mt-3 mb-3">
                        <div class="row">
                            <div class="col-10">
                                <p class="h4">
                                    Project overview & activity of
                                    <strong class="h4 text-primary">{project.title}</strong>
                                </p>
                                {#if project.short_description}
                                    <i class="text-danger">--- </i>
                                    <small class="text-muted">
                                        <strong> {project.short_description}</strong>
                                    </small>
                                {/if}
                            </div>
                            <div class="col-2 coldrop">
                                <Dropdown>
                                    <Router>
                                        <li>
                                            <Link 
                                                class="dropdown-item drop-size" 
                                                to={`/projects/${project.id}/update/`}>
                                                Update project
                                            </Link>
                                        </li>
                                        <li>
                                            <Link 
                                                to=""
                                                on:click={openAddMemberModal} 
                                                class="dropdown-item drop-size">
                                                Add member
                                            </Link>
                                        </li>
                                        <li>
                                            <Link 
                                                to=""
                                                class="dropdown-item drop-size plus-hover" 
                                                on:click={openDeleteModal}
                                                >Delete Project
                                            </Link>
                                        </li>
                                    </Router>
                                </Dropdown>
                            </div>
                        </div>
                    </div>
                {/if}
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <div class="col-6">
                            <p class="h5 text-muted">Project Statistics</p>
                        </div>
                        <hr />
                    </div>
                    <table class="table table-borderless box-shadow-none">
                        <tbody>
                            <tr>
                                <th scope="row" class="text-muted">Total test plans</th>
                                <td class="text-primary"
                                    >{project.total_test_plan.length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row" class="text-muted">Total Requirements Docs</th>
                                <td class="text-primary"
                                    >{project.total_requirements_docs
                                        .length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row" class="text-muted">Total Test Suites</th>
                                <td class="text-primary"
                                    >{project.total_suites.length}</td
                                >
                            </tr>
                            <tr>
                                <th scope="row" class="text-muted">Total Test Runs</th>
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
                                                    >--There are no incompleted
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
                                                    <strong class="text-muted"
                                                        >TestRun | 
                                                    </strong>
                                                    <a
                                                        href="/projects/{projectID}/runs/{task.id}"
                                                        class="text-center"
                                                        >{task.title}</a
                                                    >
                                                </td>
                                                <td class="text-primary">
                                                    <strong class="text-muted"
                                                        >User | 
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
                                                    >--There are no pinding tasks</td
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
            <AddProjectMemberModal
                on:message={handleAddMember}
                bind:showAddMemberModal
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
        .dropdowncustom{
            font-size: 0;
        }
        .coldrop{
            text-align: end;
            padding-right: 30px;
        }
    </style>
</svelte:head>
