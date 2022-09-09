<script>
    export let activity;
</script>



<section class="mb-4 pb-5">
    <div class="pt-5">
        <p>Recent Activity</p>
    </div>
    <div class="table pt-4">
        {#each activity as action}
        <table class="table align-middle mb-3">
                <thead class="table-bg">
                    <tr>
                        <th>
                            <span class="badge badge-success rounded-pill d-inline">{action.date}</span>
                            <span class="badge rounded-pill d-inline text-muted">Action Date</span>
                        </th>
                    </tr>
                </thead>
                <thead class="table-bg">
                    <tr>
                        <td>
                            <div class="d-inline b-0">
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
</section>
