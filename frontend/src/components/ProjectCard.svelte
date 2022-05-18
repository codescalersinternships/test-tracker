<script>
    import { Router, Link } from "svelte-navigator";
    export let title;
    export let date;
    export let link;
</script>

<div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-5 mb-md-0">
    <Router>
        <Link to={link} style="color: #000" class="text-decoration-none">
            <div class="card">
                <div class="card-body">
                    <div class="dropdown p-1" style="position: absolute;font-size: 0;right: 0;width: 30px;">
                        <a
                            class="dropdown-toggle"
                            id="dropdownMenuButton"
                            data-mdb-toggle="dropdown"
                            aria-expanded="false"
                        >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                            <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                        </svg>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <li>
                                <Link to={link} style="color: #000" class="dropdown-item">Update</Link>
                            </li>
                            <li>
                                <Link to={link} style="color: #000" class="dropdown-item">Project Member</Link>
                            </li>
                            <li>
                                <Link to={link} class="dropdown-item text-danger">Delete</Link>
                            </li>
                        </ul>
                    </div>
                    <p class="card-title h5">{title}</p>
                    <span>Created at:   </span><span class="card-subtitle mt-2 text-muted h6"> {date}</span>
                </div>
            </div>
        </Link>
    </Router>
</div>
