<script>
    export let user;
</script>

{#if user }
<div class="pt-4">
    <p class="h5">
        Projects
    </p>
    <p class="text-muted">
        {#if user.total_projects < 2}
            You are {user.type} of {user.total_projects} project
        {:else}
            You are {user.type} of {user.total_projects} projects
        {/if}
    </p>
</div>
{/if}