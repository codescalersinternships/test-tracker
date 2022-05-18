<script>
    import { Router, Route } from "svelte-navigator";
    import { onMount } from 'svelte';

    import isAuthenticated from "./healpers/IsAuthenticated"
    import axios from '././healpers/axios';
    import Logout from "./components/Logout.svelte"

    import Home from "./pages/Home.svelte";
    import Login from "./pages/Login.svelte";
    import RegisterHandeler from "./pages/RegisterHandeler.svelte";
    import Projects from "./pages/Projects.svelte";
    import ProjectDetail from "./pages/ProjectDetail.svelte";
    import MemberDetail from "./pages/MemberDetail.svelte";
    import Members from "./pages/Members.svelte";
    import NotFound from "./pages/NotFound.svelte";

    let user;
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };
    onMount(async () => {
        isAuthenticated();
        const userDetails = await axios.get('/dashboard/total_projects/', config);
        user = await userDetails.data.data
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
        <Route path="/" primary={false}><Home user={user}/></Route>
        <Route path="projects/" primary={false}><Projects user={user}/></Route>
        <Route path="projects/:id/" primary={false}><ProjectDetail user={user}/></Route>
        <Route path="auth/login/" primary={false}><Login/></Route>
        <Route path="auth/register/" primary={false}><RegisterHandeler/></Route>
        <Route path="members/" primary={false}><Members user={user}/></Route>
        <Route path="members/:id/" primary={false}><MemberDetail user={user}/></Route>
        <Route path="auth/logout/" primary={false}><Logout/></Route>
        <Route> 
            <NotFound/>
        </Route>
    </Router>
</main>
