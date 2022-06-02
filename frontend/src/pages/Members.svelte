<script>
    import { onMount } from 'svelte';
    import { Link } from "svelte-navigator";

    import axios from '../healpers/axios'

    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"

    export let user;

    let members, membersCopy, thisMember;
    let show = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    onMount(async () => {
        try {
            const response = await axios.get('/members/all/', config)
            members = await response.data.data
            membersCopy = members
        } catch (err) {
            if (err.response.status === 403){
                window.location.href = '/not-found'
            }
        }
    });

    async function handleDelete(event) {
        const member = event.detail.obj;
        const indx = members.findIndex(v => v.id === member.id);
        members = members;
        members.splice(indx, 1);
    }

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        members = searchProjects;
    }

    function setMember(member) {
        thisMember = member
        show = true;
    }
</script>

<svelte:head>
    <title>Test-Tracker | Members</title>
    <style>
        .user_photo{
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

        .info_user strong{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #5a79b1;
        }
    </style>
</svelte:head>

<section>
    {#if user}
        <NavBar user={user}/>
        <div class="container pt-4 pb-4">
            {#if members}
                <div class="">
                    <strong class="h4">All Members</strong>
                    <br>
                    -- There are <strong>{members.length}</strong> {user.total_projects === 1 ? 'member' : 'members'} registered
                </div>
                <div class="pt-4">
                    <p>
                        Search Members
                    </p>
                    <Search request="/members/search/" objects={members} config={config} objectsCopy={membersCopy} on:message={handleSearch}/>
                </div>
                <div class="pt-5">
                    <div class="row">
                        {#each members as member}
                            <div class="col-12 mb-4">
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
                                                <button class="dropdown-item text-danger" on:click={setMember(member)}>Delete</button>
                                            </li>
                                        </ul>
                                    </div>
                                    <Link to="/members/{member.id}/" class="text-dark d-block text-decoration-none">
                                        <div class="card-body d-flex align-items-center">
                                            <span class="user_photo">
                                                {member.first_name[0]}{member.last_name[0]}
                                            </span>
                                            <div class="info_user">
                                                <strong>{member.full_name}</strong>
                                                <p class="text-muted mb-0">Member since: {member.created}</p>
                                            </div>
                                        </div>
                                    </Link>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            {:else}
                <div class="col-12 pt-5">
                    <p class="text-muted">
                        -- There are no members
                    </p>
                </div>
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
    <DeleteModal
        bind:show
        on:message={handleDelete}
        obj={thisMember}
        onRequest='/members'
        config={config}
    />
</section>