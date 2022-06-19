<script>
    import { Router, Route, links } from "svelte-navigator";
    import { onMount } from 'svelte';

    import isAuthenticated from "./healpers/IsAuthenticated"
    import axios from './healpers/axios';
    
    import Home from "./pages/Home.svelte";
    
    import Login from "./pages/Login.svelte";
    import Logout from "./components/Logout.svelte"
    import RegisterHandeler from "./pages/RegisterHandeler.svelte";

    import Projects from "./pages/Projects.svelte";
    import ProjectDetails from "./pages/ProjectDetails.svelte";
    import UpdateProject from "./pages/UpdateProject.svelte";

    import Members from "./pages/Members.svelte";
    import MemberDetails from "./pages/MemberDetails.svelte";

    import Requirements from "./pages/Requirements.svelte";
    import RequirementsDetails from "./pages/RequirementsDetails.svelte";

    import TestPlans from "./pages/TestPlans.svelte";
    import TestPlanDetails from "./pages/TestPlanDetails.svelte";

    import TestSuite from "./pages/TestSuite.svelte";
    import TestSuiteDetails from "./pages/TestSuiteDetails.svelte";

    import TestRun from "./pages/TestRun.svelte";
    import TestRunDeetails from "./pages/TestRunDeetails.svelte";

    import NotFound from "./pages/NotFound.svelte";

    let user;
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };
    onMount(async () => {
        isAuthenticated();
        const userDetails = await axios.get('/dashboard/user/', config);
        user = await userDetails.data.data
    });

</script>
<svelte:head>
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
        >
    </script>
    <style>
        body {
            padding: 0 8px !important;
        }
        .form-check-input[type=radio]:after {
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%)
        }
        .form-check-input:checked:before,
        .form-check-input:before{
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%)
        }
        .plus-background{
            background: #bf4e62;
        }
        .plus-color{
            color: #bf4e62;
        }
        .plus-hover{
            padding: 15px;
        }
        .plus-hover:hover{
            background: #bf4e62;
            color: #fff;
        }
        .form-check-input:checked:focus:before,
        .form-check-input:focus:before {
            transform: scale(1) translate(-50%, -50%);
        }
        .modal{
            background: #0e1117a3;
        }
        .link-color: {
            color: #5a79b1;
        }
    </style>
</svelte:head>

<main>
    <Router>
        <Route path="/" primary={false}><Home user={user}/></Route>
        <Route path="auth/login/" primary={false}><Login/></Route>
        <Route path="auth/register/" primary={false}><RegisterHandeler/></Route>
        <Route path="auth/logout/" primary={false}><Logout/></Route>
        
        <Route path="projects/" primary={false}><Projects user={user}/></Route>
        <Route path="projects/:id/" primary={false}><ProjectDetails user={user}/></Route>
        <Route path="projects/:id/update/" primary={false}><UpdateProject user={user}/></Route>

        <Route path="projects/:id/test-plans/" primary={false}><TestPlans user={user}/></Route>
        <Route path="projects/:id/test-plans/:id/" primary={false}><TestPlanDetails user={user}/></Route>

        <Route path="projects/:id/requirements/" primary={false}><Requirements user={user}/></Route>
        <Route path="projects/:id/requirements/:id/" primary={false}><RequirementsDetails user={user}/></Route>

        <Route path="projects/:id/test-suites/" primary={false}><TestSuite user={user}/></Route>
        <Route path="projects/:id/test-suites/:id/" primary={false}><TestSuiteDetails user={user}/></Route>
        
        <Route path="members/" primary={false}><Members user={user}/></Route>
        <Route path="members/:id/" primary={false}><MemberDetails user={user}/></Route>
        
        <Route path="projects/:id/runs/" primary={false}><TestRun user={user}/></Route>
        <Route path="projects/:id/runs/:id/" primary={false}><TestRunDeetails user={user}/></Route>

        <Route> 
            <NotFound/>
        </Route>
    </Router>
</main>
