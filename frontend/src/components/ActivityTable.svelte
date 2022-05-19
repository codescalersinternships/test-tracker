<script>
    export let activity;
</script>



<section class="mb-4 pb-5">
    <div class="pt-5">
        <p>Activity</p>
    </div>
    {#if activity}
        <div class="table pt-4">
            {#each activity as action}
                <table class="table align-middle mb-3 bg-white">
                    <thead class="bg-light">
                        <tr>
                            <th><span class="badge badge-success rounded-pill d-inline">{action.date}</span></th>
                        </tr>
                    </thead>
                    <thead class="bg-light">
                        <tr>
                            <td>
                                <div class="d-inline">
                                    <div class="ms-3">
                                        <p class="text-muted mb-0">{action.action}</p>
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
