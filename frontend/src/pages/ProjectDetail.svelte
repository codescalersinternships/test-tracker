<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'
    import NavBar from "../components/NavBar.svelte";
    import ActivityTable from "../components/ActivityTable.svelte"
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte"

    export let user;
    let project, activity;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };
    
    onMount(async () => {
        var path = window.location.pathname;
        var lastSlash = path.lastIndexOf('/');
        var projectID = path.substring(lastSlash + 1);
        try {
            const response = await axios.get(`project/${projectID}/`, config)
            project = await response.data.data;
            activity = project.activity
        }catch(err) {
            if(err.response.status === 404 || err.response.status === 403){
                window.location.href = '/not-found'
            }
        }
    })
</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    {#if user && project}
        <NavBar projectView="true" user={user}/>
        <div class="container">
            <div class="pt-5">
                <strong class="h4">Project overview & activity of {project.name}</strong>
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <p class="h5 text-muted">Project statistics</p>
                        <hr>
                        <table class="table table-borderless">
                            <tbody>
                                <tr>
                                <th scope="row">Total test plans</th>
                                <td class="text-primary">{project.total_test_plan.length}</td>
                                </tr>
                                <tr>
                                <th scope="row">Total Requirements Docs</th>
                                <td class="text-primary">{project.total_requirements_docs.length}</td>
                                </tr>
                                <tr>
                                <th scope="row">Total Test Suites</th>
                                <td class="text-primary">{project.total_suites.length}</td>
                                </tr>
                                <tr>
                                <th scope="row">Total Test Runs</th>
                                <td class="text-primary">{project.total_test_runs.length}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card mt-4 p-4">
                    <div class="pt-4">
                        <div class="row">
                            <div class="col-6">
                                <p class="h5 text-muted">Incomplete test runs assigned to you</p>
                            </div>
                            <div class="col-6 text-muted">
                                <p class="h5">People with the most incomplete test runs</p>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-6">
                                <table class="table table-borderless">
                                    {#each project.incomplete_test_runs_assigned_to_you as task }
                                        <tbody>
                                        <tr>
                                            <th scope="row">{task.title}</th>
                                            <td class="text-primary">{task.created}</td>
                                        </tr>
                                        </tbody>
                                    {:else}
                                        <tbody>
                                        <tr>
                                            <td class="text-muted">There are no incompleted task for you</td>
                                        </tr>
                                        </tbody>
                                    {/each}
                                </table>
                            </div>
                            <div class="col-6">
                                <table class="table table-borderless">
                                    {#each project.people_with_the_most_incomplete_test_runs as task }
                                        <tbody>
                                        <tr>
                                            <th scope="row">{task.title}</th>
                                            <td class="text-primary">
                                                <a href="/members/{task.assigned_user.id}">{task.assigned_user.full_name}</a>
                                            </td>
                                        </tr>
                                        </tbody>
                                    {:else}
                                        <tbody>
                                        <tr>
                                            <td class="text-muted">There are no pinding tasks</td>
                                        </tr>
                                        </tbody>
                                    {/each}
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <ActivityTable activity={activity} />
            </div>
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
</section>
