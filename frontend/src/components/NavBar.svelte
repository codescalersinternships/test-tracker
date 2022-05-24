<script>
        import { Router, Link } from "svelte-navigator";
        export let projectView = false;
        export let user;

        let projectID;

        if (projectView) {
            let path = window.location.pathname;
            projectID = path.split("/")[2];
        }

</script>

<svelte:head>
    <style>
        .user_photo_nav{
            display: inline-block;
            background: #5a79b1;
            margin-right: 15px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            line-height: 40px;
            text-align: center;
            color: #fff;
        }
    </style>
</svelte:head>

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
                    {#if user.permission == "admin"}
                        <li class="nav-item">
                            <Link to="/members/" class="nav-link">Members</Link>
                        </li>
                    {/if}
                    {#if projectView && projectID}
                        <li class="nav-item">
                            <Link to="/projects" class="nav-link">Projects</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/projects/{projectID}/test-plans/" class="nav-link">Test Plans</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/projects/{projectID}/requirements/" class="nav-link">Requirements</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/projects/{projectID}/test-suites/" class="nav-link">Test Suite</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/test-runs/" class="nav-link">Test Runs</Link>
                        </li>
                    {:else}
                        <li class="nav-item">
                            <Link to="/projects" class="nav-link">Projects</Link>
                        </li>
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
                <span class="user_photo_nav">
                    {user.first_name[0]}{user.last_name[0]}
                </span>
                <!-- {user.full_name} -->
                </a>
                <ul
                    class="dropdown-menu dropdown-menu-end"
                    aria-labelledby="navbarDropdownMenuAvatar"
                >
                {#if user.type != "admin"}
                    <li>
                        <a class="dropdown-item text-primary" href="/members/{user.id}">{user.full_name}</a>
                    </li>
                {/if}
                    <li>
                        <a class="dropdown-item text-primary" href="#">Settings</a>
                    </li>
                    <li>
                        <a class="dropdown-item text-primary" href="/auth/logout/">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</nav>
