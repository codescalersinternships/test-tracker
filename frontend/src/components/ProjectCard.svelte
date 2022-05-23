<script>
    import { Link } from "svelte-navigator";

    export let project;

</script>
{#if project}
    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-5 mb-md-0">
        <div class="card">
            <div class="dropdown p-1" style="position: absolute;font-size: 0;right: 0; top: 20px;">
                <a
                    class="dropdown-toggle"
                    id="dropdownMenuButton"
                    data-mdb-toggle="dropdown"
                    aria-expanded="false"
                    >
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                        <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                    </svg>
                </a>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <li>
                        <slot></slot>
                    </li>
                </ul>
            </div>
            <Link to="/projects/{project.id}/" class="text-dark text-decoration-none">
                <div class="card-body">
                    <p class="card-title h5">{project.title.length > 25 ? project.title.slice(0,25)+'..' : project.title}</p>
                    <span>Created at:   </span><span class="card-subtitle mt-2 text-muted h6"> {project.created}</span>
                </div>
            </Link>
        </div>
    </div>
{/if}