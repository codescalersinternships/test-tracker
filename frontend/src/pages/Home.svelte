<script>
    import NavBar from "../components/NavBar.svelte";
    import TotalProjectsLength from "../components/ui/TotalProjectsLength.svelte";
    import Projects from "../components/Projects.svelte";
    import ActivityTable from "../components/ActivityTable.svelte";

</script>

<svelte:head>
    <title>Test-Tracker</title>
</svelte:head>

<section>
    <NavBar />
    <div class="container">
        <TotalProjectsLength/>
        <Projects endPoint='/project/last-5-projects/' pageTitle="Latest Projects"/>
        <ActivityTable endPoint='/project/last-5-projects/activity/'/>
    </div>
</section>