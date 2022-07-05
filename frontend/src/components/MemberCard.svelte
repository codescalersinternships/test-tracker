<script>
    import Dropdown from "../components/ui/Dropdown.svelte";
    import { Router, Link } from "svelte-navigator";

    export let member;
    let invited = member.invited && !member.accepted;
</script>

<div class="col-12 mb-4">
    <div class="card">
        <div class="coldrop">
            <Dropdown>
                <Router>
                    <li>
                        <slot></slot>
                    </li>
                </Router>
            </Dropdown>
        </div>
        <Link
            to="/members/{member.id}/"
            class="d-block text-decoration-none"
        >
            <div
                class="card-body d-flex align-items-center"
                class:invited="{invited === true}"
            >
                <span class="user_photo">
                    {member.first_name[0]}{member
                        .last_name[0]}
                </span>
                <div class="info_user">
                    <strong
                        >{member.full_name}</strong
                    >
                    {#if invited}
                        <p class="text-muted mb-0">
                            invited...
                        </p>
                    {:else}
                        <p class="text-muted mb-0">
                            Member since: {member.created}
                        </p>                       
                    {/if}
                </div>
            </div>
        </Link>
    </div>
</div>

<svelte:head>
    <style>
        .coldrop{
            position: absolute;
            font-size: 0;
            right: 0; 
            top: 20px;
        }
        .user_photo {
            display: inline-block;
            background: #5a79b1;
            margin-right: 15px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            line-height: 60px;
            text-align: center;
            font-weight: 900;
            color: #fff;
        }
        .info_user {
            flex: 1;
        }

        .info_user strong {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #5a79b1;
        }

    </style>
</svelte:head>