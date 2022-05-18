<script>
    import { Router, Route } from "svelte-navigator";
    import { onMount } from 'svelte';

    import isAuthenticated from "./healpers/IsAuthenticated"

    import Home from "./pages/Home.svelte";
    import Login from "./pages/Login.svelte";
    import RegisterHandeler from "./pages/RegisterHandeler.svelte";
    import Projects from "./pages/Projects.svelte";
    import ProjectDetail from "./pages/ProjectDetail.svelte";
    import MemberDetail from "./pages/MemberDetail.svelte";
    import People from "./pages/Members.svelte";
    import NotFound from "./pages/NotFound.svelte";

    onMount(() => {
        isAuthenticated();
    });

</script>
<svelte:head>
    <title>THis Is Test</title>
    <!-- Font Awesome -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    rel="stylesheet"
    />
    <!-- Google Fonts -->
    <link
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
    rel="stylesheet"
    />
    <!-- MDB -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.css"
    rel="stylesheet"
    />
    <script
        type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.js"
        defer
    ></script>
    <style>
        body {
            padding: 0 8px !important;
        }
    </style>
</svelte:head>

<main>
    <Router>
        <Route path="/" primary={false}><Home /></Route>
        <Route path="auth/login/" primary={false}><Login/></Route>
        <Route path="auth/register/" primary={false}><RegisterHandeler/></Route>
        <Route path="projects/" primary={false}><Projects/></Route>
        <Route path="projects/:id/" primary={false}><ProjectDetail/></Route>
        <Route path="members/" primary={false}><People/></Route>
        <Route path="members/:id/" primary={false}><MemberDetail/></Route>
        <Route> 
            <NotFound/>
        </Route>
    </Router>
</main>
