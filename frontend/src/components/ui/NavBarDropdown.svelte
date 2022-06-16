<script>
    import { Router, Link } from "svelte-navigator";
</script>


<div class="d-flex align-items-center">
    <div class="dropdown">
        <Router>
            <Link
                class="dropdown-toggle d-flex align-items-center hidden-arrow"
                to="#"
                id="navbarDropdownMenuAvatar"
                role="button"
                data-mdb-toggle="dropdown"
                aria-expanded="false"
                >
                <slot name="dropdown-toggle"></slot>
            </Link>
        </Router>
        <ul
            class="dropdown-menu dropdown-menu-end"
            aria-labelledby="navbarDropdownMenuAvatar"
        >
            <slot name="dropdown-li"></slot>
        </ul>
    </div>
</div>

<svelte:head>
    <style>
        .user_photo_nav{
            display: inline-block;
            background: #5a79b1;
            margin-right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            line-height: 40px;
            text-align: center;
            color: #fff;
        }
        a{
            text-decoration: none !important;
            color: #5a79b1 !important;
        }
        .add-obj{
            background: #bf4e62;
                line-height: 42px;
                font-size: 28px;
        }
    </style>
</svelte:head>