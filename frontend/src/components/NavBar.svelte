<script>
        import { Router, Link } from "svelte-navigator";
        import { onMount } from 'svelte';
        import JWTPars from "../healpers/JWTPars"
        import axios from '../healpers/axios';

        export let projectView = false;

        let user = {}
        let userType;
        const config = {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        };

        onMount(async () => {
            try {
                const email = JWTPars(localStorage.getItem("token"))["email"];
                const response = await axios.get(`/auth/users/${email}/`)
                const uType = await axios.get('/dashboard/total_projects/', config)
                userType = uType.data.data.type
            if (response.status === 200) { user = response.data.data }} 
            catch(err) {
                console.log(err);
                // window.location.href = '/auth/login/'
            }
            return user
        });
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <button
            class="navbar-toggler"
            type="button"
            data-mdb-toggle="collapse"
            data-mdb-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
        <i class="fas fa-bars"></i>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <Link to="/" class="nav-link text-primary">Dashboard</Link>
                </li>
                <Router>
                    {#if projectView}
                        <li class="nav-item">
                            <Link to="/projects" class="nav-link">Projects</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/test-plans/" class="nav-link">Test Plans</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/requirements/" class="nav-link">Requirements</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/test-suites/" class="nav-link">Test Suite</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/test-runs/" class="nav-link">Test Runs</Link>
                        </li>
                        {:else}
                        <li class="nav-item">
                            <Link to="/projects" class="nav-link">Projects</Link>
                        </li>
                        {#if userType == "admin"}
                            <li class="nav-item">
                                <Link to="/members/" class="nav-link">Members</Link>
                            </li>
                        {/if}
                        <li class="nav-item">
                            <Link to="/overview/" class="nav-link">Settings</Link>
                        </li>
                    {/if}
                </Router>
            </ul>
        </div>
        <div class="d-flex align-items-center">
            <div class="dropdown">
                <a
                    class="dropdown-toggle d-flex align-items-center hidden-arrow"
                    href="#"
                    id="navbarDropdownMenuAvatar"
                    role="button"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                >
                {user.full_name}
                </a>
                <ul
                    class="dropdown-menu dropdown-menu-end"
                    aria-labelledby="navbarDropdownMenuAvatar"
                >
                    <li>
                        <a class="dropdown-item" href="#">{user.full_name}</a>
                    </li>
                    <li>
                        <a class="dropdown-item" href="#">Settings</a>
                    </li>
                    <li>
                        <a class="dropdown-item" href="#">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>
