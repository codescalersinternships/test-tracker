<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';

    export let endPoint;

    let activityTable;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const response = await axios.get(endPoint, config)
        if (response.data.data.length > 0){
            activityTable = response.data.data
        }
        return activityTable
    });
</script>



<section class="mb-4 pb-5">
    <div class="pt-5">
        <p>Activity</p>
    </div>
    {#if activityTable}
        <div class="table pt-4">
            {#each activityTable as activity}
                <table class="table align-middle mb-3 bg-white">
                    <thead class="bg-light">
                        <tr>
                            <th><span class="badge badge-success rounded-pill d-inline">{activity.date}</span></th>
                        </tr>
                    </thead>
                    <thead class="bg-light">
                        <tr>
                            <td>
                                <div class="d-inline">
                                    <div class="ms-3">
                                        <p class="text-muted mb-0">{activity.action}</p>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </thead>
                </table>
            {/each}
        </div>
    {:else}
        <div class="col-12">
            <p class="text-muted">
                -- There are no activity yet
            </p>
        </div>
    {/if}
</section>
