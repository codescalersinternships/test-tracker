<script>
    import { onMount } from "svelte";
    import { Link } from "svelte-navigator";
    import axios from "../healpers/axios";

    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import MemberCard from "../components/MemberCard.svelte";

    export let user;

    let members, membersCopy, thisMember;
    let showDeleteModal = false;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        try {
            const response = await axios.get("/members/all/", config);
            members = await response.data.data;
            membersCopy = members;
        } catch (err) {
            if (err.response.status === 403) {
                window.location.href = "/not-found";
            }
        }
    });

    async function handleDelete(event) {
        const member = event.detail.obj;
        const indx = members.findIndex((v) => v.id === member.id);
        members = members;
        members.splice(indx, 1);
    }

    async function handleSearch(event) {
        const searchProjects = event.detail.objects;
        members = searchProjects;
    }

    function setMember(member) {
        thisMember = member;
        showDeleteModal = true;
    }
</script>

<svelte:head>
    <title>Test-Tracker | Members</title>
</svelte:head>

<section>
    {#if user}
        <NavBar {user} />
        <div class="container pt-4 pb-4">
            {#if members}
                <div class="">
                    <strong class="h4">All Members</strong>
                    <br />
                    -- There are <strong>{members.length}</strong>
                    {user.total_projects === 1 ? "member" : "members"} registered
                </div>
                <div class="pt-4">
                    <p>Search Members</p>
                    <Search
                        request="/members/search/"
                        objects={members}
                        {config}
                        objectsCopy={membersCopy}
                        on:message={handleSearch}
                    />
                </div>
                <div class="pt-5">
                    <div class="row">
                        {#each members as member}
                            <MemberCard {member}>
                                <Link 
                                    to=""
                                    class="dropdown-item text-danger" 
                                    on:click={setMember(member)}
                                    >Delete {member.first_name}
                                </Link>
                            </MemberCard>
                        {/each}
                    </div>
                </div>
            {:else}
                <div class="col-12 pt-5">
                    <p class="text-muted">-- There are no members</p>
                </div>
            {/if}
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={thisMember}
        onRequest="/members"
        {config}
    />
</section>
