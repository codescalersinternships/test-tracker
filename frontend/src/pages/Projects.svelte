<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'

    import NavBar from "../components/NavBar.svelte";
    import Projects from "../components/Projects.svelte";
    import TotalProjectsLength from "../components/ui/TotalProjectsLength.svelte";

</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    <NavBar projectView="true"/>
    <div class="container">
        <TotalProjectsLength/>
        <Projects allOfProjects = "/dashboard/projects/" pageTitle="All Projects"/>
    </div>
</section>