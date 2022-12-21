<script>
    import { Router, Route } from "svelte-navigator";
    import { onMount } from 'svelte';

    import isAuthenticated from "./healpers/IsAuthenticated"
    import axios from './healpers/axios';
    import { setTheme } from './healpers/theme';
    
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
    import RunTestRun from "./pages/RunTestRun.svelte";

    import Settings from "./pages/Settings.svelte";
    import NotFound from "./pages/NotFound.svelte";

    let user;
    const mode = localStorage.getItem("mode")

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };
    onMount(async () => {
        setTheme(mode);
        isAuthenticated();
        console.log("watch");
        const userDetails = await axios.get('/dashboard/user/', config);
        console.log(userDetails.status);
        user = await userDetails.data.data
        if (!user) {
            return {
                status: 302,
                redirect: "/login"
            };
        }
    });

</script>

<main>
    <Router>
        <Route path="/" primary={false}><Home user={user}/></Route>
        <Route path="settings/" primary={false}><Settings user={user}/></Route>

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
        <Route path="projects/:id/runs/:id/run" primary={false}><RunTestRun user={user}/></Route>

        <Route> 
            <NotFound/>
        </Route>
    </Router>
</main>


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
        :root{
            --bg-color: #f1f1f1;
            --text-color: #000;
            --boxes-bg: #fff;
            --boxes-shadow: 0px 2px 6px #00000030;
            --text-muted: #757575;
            --text-primary: #5a79b1;
            --text-primary-10: #5a79b1ab;
            --text-primary-5: #5a79b178;
            --text-danger: #bf4e62;
            --text-light: #fff;
            --text-dark: #222;
            --calender-today: rgb(255 169 0 / 36%);
        }
        .bill-today{
            background: var(--calender-today);
        }
        body{
            color: var(--text-color);
            background-color: var(--bg-color);
        }
        .text-muted{
            color: var(--text-muted)!important;
        }
        .selected-suite{
            background: var(--bg-color);
            color: var(--text-color);
            border: solid 1px var(--text-primary)!important;
        }
        .suites-selected-button {
            border-radius: 0px;
            background-color: var(--boxes-bg);
            box-shadow: var(--boxes-shadow);
            border: 0;
        }
        .suites-selected-button:focus {
            background: var(--bg-color)!important;
            border-color: var(--text-danger);
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
        .dropdown-menu{
            margin-top: 15px!important;
            background: var(--boxes-bg);
            border: 1px solid var(--text-primary);
            border-radius: 5px;
        }
        .dropdown-item{
            border-radius: 5px !important;
        }
        .setting-drop{
            border-radius: 0px!important;
            color: var(--text-primary)!important;
            padding: 15px;
        }
        .setting-drop:hover{
            background: var(--text-primary) !important;
            color: var(--text-light) !important;
        }
        .plus-background{
            background: var(--text-danger) !important;
        }
        .plus-color{
            color: var(--text-danger);
            border-radius: 0px!important;
        }
        .plus-hover{
            padding: 15px;
        }
        .drop-size{
            padding: 15px;
            border-radius: 0px!important;
        }
        .drop-size:hover{
            background: var(--text-primary);
            color: var(--text-light)!important;
        }
        .delete-drop{
            background:var(--boxes-bg)!important;
            padding: 15px;
            color: var(--text-danger);
        }
        .delete-drop:hover{
            color: #fff;
            background-color: var(--text-danger);
        }
        .plus-hover:hover{
            background: var(--text-danger);
            color: var(--text-light);
        }
        .plus-hover:focus{
            background: var(--text-danger) !important;
            color: var(--text-light) !important;
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
        .width-100{
            width: 100%;
        }
        .text-primary{
            color:var(--text-primary) !important;
        }
        .btn-primary{
            background:var(--text-primary) !important;
        }
        .user_photo_nav{
            display: inline-block;
            background: var(--text-primary);
            margin-right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            line-height: 40px;
            text-align: center;
            color: #fff;
            font-weight: 700;
        }
        .not_run {
            background-color: var(--text-primary);
        }
        .user_photo {
            margin-right: 15px;
            width: 60px;
            height: 60px;
            line-height: 60px;
            text-align: center;
        }
        .svg {
            color: var(--text-primary) !important;
            margin-bottom: 3px;
        }
        .calnder-chart {
            border: none;
            outline: none;
            background-color: var(--bg-color);
            color: var(--text-color) !important;
            position: relative;
        }
        .calnder-char-today {
            background-color: var(--calender-today);
        }
        .calnder-chart-bg {
            background-color: var(--bg-color);
            color: var(--text-color) !important;
        }
        .col-filter-run-btn{
            padding: 10px;
            width: 100%;
            border: 1px solid var(--text-primary) !important;
            border-radius: 2px;
        }
        .col-filter-run-btn:focus{
            background:var(--bg-color) !important;
        }
        .btn-outline-primary{
            border:solid 1px #5a79b1!important;
            color:var(--text-primary) !important;
        }
        .background-primary{
            background:#5a79b1!important;
        }
        .card{
            border-radius: 0px;
            background-color: var(--boxes-bg);
            box-shadow: var(--boxes-shadow);
            border: 0 !important;
        }
        .table-bg{
            border-radius: 0px;
            background-color: var(--boxes-bg);
            box-shadow: var(--boxes-shadow);
            border: 0 !important;
        }
        .table>:not(caption)>*>* {
            background-color: var(--boxes-bg);
            border-bottom-width: 0px;
        }
        .navbar{
            background-color: var(--boxes-bg) !important;
            box-shadow: var(--boxes-shadow);
            border: 0 !important;
        }
        .modal-content{
            background-color: var(--boxes-bg)!important;
            box-shadow: var(--boxes-shadow)!important;
            border: 0 !important;
        }
        .nav-tabs{
            background-color: var(--boxes-bg)!important;
            box-shadow: var(--boxes-shadow)!important;
            border: 0 !important;
        }
        .nav-link{
            color: var(--text-primary) !important;
        }
        .nav-link-tab:hover{
            background-color: var(--bg-color)!important;
            box-shadow: var(--boxes-shadow)!important;
        }
        .nav-link.active {
            background-color: var(--bg-color)!important;
            box-shadow: none!important;
            border: 0 !important;
            border-bottom: 2px solid var(--text-primary) !important;
        }
        .input{
            outline: none !important;
            margin-right: 3px !important;
            background-color: var(--bg-color);
            border: 1px solid var(--text-primary) !important;
            border-radius: 3px !important;
            color: var(--text-color);
        }
        input:disabled {
            background-color: var(--boxes-bg) !important;
            color: var(--text-dark-color);
        }
        .form-control:focus {
            box-shadow: none;
            border-color: none;
            box-shadow: var(--boxes-shadow);
            background-color: var(--boxes-bg);
            color: var(--text-color);
        }
        .light{
            background: var(--bg-color);
            color: var(--text-color);
            transition: 0.3s
        }
        .sun-btn{
            background: var(--bg-color)!important;
            box-shadow: var(--boxes-shadow);
        }
        .moon-btn {
            box-shadow: var(--boxes-shadow);
            background: var(--bg-color)!important;
        }
        .sun-btn:focus{
            background: var(--bg-color)!important;
            box-shadow: none;
        }
        .moon-btn:focus{
            background: var(--bg-color)!important;
            box-shadow: none;
        }
        .badge-success {
            background-color: var(--text-primary)!important;
            color: #fff;
            border-radius: 4px;
            float: right;
        }
        .bill-15{
            background: var(--text-primary);
        }
        .bill-10{
            background: var(--text-primary-10);
        }
        .bill-5{
            background: var(--text-primary-5);
        }
        .check-box{
            width: 70px;
            height: 40px;
            background: rgb(255, 255, 255);
            border-radius: 50px;
            cursor: pointer;
            border: 1px solid var(--text-primary);
            position: relative;
        }
        .checkbox-span{
            content: "";
            position: absolute;
            border: none;
            z-index: 2;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            background-color: var(--text-primary);
            box-shadow: 0 3px 1px -2px rgb(0 0 0 / 20%), 0 2px 2px 0 rgb(0 0 0 / 14%), 0 1px 5px 0 rgb(0 0 0 / 12%);
            transition: background-color .2s,transform .2s;
            top: 50%;
            transform: translateY(-50%)
        }
        .checkbox-span:not(.checkbox-span-checked) {
            left: 5px;
        }
        .checkbox-span-checked{
            background-color: var(--text-light)!important;
            right: 5px;
        }
        .checkbox--checked{
            border: 1px solid var(--text-light) !important;
            background-color: var(--text-primary) !important;
        }
        .p-relative{
            position: relative;
        }
        .p-abs{
            position: absolute;
        }
        .right-0{
            right: 0px
        }
        .new-section-button{
            border: 1px solid var(--text-primary);
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        .new-section-button-api{
            border: 1px solid var(--text-primary);
            background-color: var(--bg-color);
            color: var(--text-color);
            width: 100%;
        }
        .default-text-color{
            color: var(--text-color);
        }
        .cases-card{
            width: 80%;
            margin: 0 auto;
        }
        .over-scroll{
            height: 300px;
            overflow-y: scroll;
            padding: 15px 0;
        }
        .case-content{
            width: 95%;
            margin: 0 auto 6px;
            border-radius: 0px !important;
        }
        .cases-lines{
            border: 1px solid var(--text-primary);
            padding: 10px;
        }
        .case-content:last-child {
            margin-bottom:0;
        }
        .new-section-button:hover{
            border: 1px solid var(--bg-color);
            background-color: var(--text-primary);
            color: var(--text-light);
            transition: 0.3s;
        }
        .new-section-clicked{
            display: none !important;
        }
        .list-item {
            display: block;
            cursor: move;
            margin-bottom: 20px!important;
        }
        .list-item.is-active {
            background-color: var(--text-primary) !important;
            color: var(--text-color);
            padding: 10px;
            padding-bottom: 10px;
            margin-bottom: 15px;
            border-radius: 15px;
        }
        .new-test-case{
            margin-top: 15px;
            border-left: 4px solid var(--text-primary) !important;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 15px;
        }
        .dark{
            transition: 0.3s;
            --bg-color: #1a1a1a;
            --text-color: #fff;
            --boxes-bg: #262626;
            --boxes-shadow: 0px 0px 2px 2px #4a4a4a;
            --text-muted: #ebe7e7;
            --text-primary: #1da1f2;
            --text-primary-10: #1da1f296;
            --text-primary-5: #1da1f242;
            --calender-today: rgb(255 169 0 / 10%);
        }
    </style>
</svelte:head>