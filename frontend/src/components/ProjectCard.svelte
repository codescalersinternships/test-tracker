<script>
    import { Link } from "svelte-navigator";
    import Dropdown from "./ui/Dropdown.svelte";

    export let project;

</script>

{#if project}
    <div class="col-12 col-md-6 col-lg-4 col-xl-3 mb-5 mb-md-2">
        <div class="card">
            <Dropdown>
                <li>
                    <slot></slot>
                </li>
            </Dropdown>
            <Link to="/projects/{project.id}/" class="text-dark text-decoration-none">
                <div class="card-body">
                    <p class="card-title h5">{project.title.length > 25 ? project.title.slice(0,25)+'..' : project.title}</p>
                    <span>Created at:   </span><span class="card-subtitle mt-2 text-muted h6"> {project.created}</span>
                </div>
            </Link>
        </div>
    </div>
{/if}

<svelte:head>
    <style>
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            top:20px
        }
    </style>
</svelte:head>