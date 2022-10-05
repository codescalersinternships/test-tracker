<script>
        import { createEventDispatcher } from 'svelte';
        import { Router, Link } from "svelte-navigator";
        import NavBarDropdown from './ui/NavBarDropdown.svelte'
        import AddNewObject from './AddNewObject.svelte'

        export let projectView = false;
        export let user;
        const dispatch = createEventDispatcher();

        let projectID;

        if (projectView) {
            let path = window.location.pathname;
            projectID = path.split("/")[2];
        }
</script>

<svelte:head>
    <style>
        a{
            text-decoration: none !important;
            color: #5a79b1 !important;
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
                <Router>
                    <li class="nav-item">
                        <Link to="/" class="nav-link">Dashboard</Link>
                    </li>
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
                            <Link to="/projects/{projectID}/test-suites/" class="nav-link">Test Suites</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/projects/{projectID}/runs/" class="nav-link">Test Runs</Link>
                        </li>
                    {:else}
                        <li class="nav-item">
                            <Link to="/projects" class="nav-link">Projects</Link>
                        </li>
                        <li class="nav-item">
                            <Link to="/settings/" class="nav-link">Settings</Link>
                        </li>
                    {/if}
                </Router>
            </ul>
        </div>
        <AddNewObject 
            on:message={(event) => {
                dispatch('message', {
                    obj: event.detail.obj,
                });
            }}
        />
        <NavBarDropdown>
            <span slot="dropdown-toggle" 
                class="user_photo_nav">
                {#if user.first_name}
                    {user.first_name[0]}{user.last_name[0]}
                {:else}
                    {user.email[0]}
                {/if}
            </span>
            <span slot="dropdown-li">
                <li>
                    <Link to="/settings/" class="dropdown-item setting-drop">Settings</Link>
                </li>
                <li>
                    <Link to="/auth/logout/" class="dropdown-item setting-drop">Logout</Link>
                </li>
            </span>
        </NavBarDropdown>
    </div>
</nav>
