<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'

    import ProjectCard from "./ProjectCard.svelte";

    let projects = [];
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        const response = await axios.get('/dashboard/projects/', config)
        projects = response.data.data
        for (let project of projects) {
            project.name = project.name.slice(0,25)
        }
        return projects
    });
</script>

<section>
    <div class="pt-5 last-projects">
        <p>All Projects</p>
        <div class="row p-1">
            {#each projects as project}
                {#if project.name.length > 25}
                    <ProjectCard title={project.name.slice(0,25)+'..'} date={project.created} link={`/projects/${project.id}`}/>
                {:else}
                    <ProjectCard title={project.name} date={project.created} link={`/projects/${project.id}`}/>
                {/if}
            {:else}
                <div class="col-12">
                    <p class="text-muted">
                        -- There are no projects yet
                    </p>
                </div>
            {/each}
        </div>
    </div>    
</section>