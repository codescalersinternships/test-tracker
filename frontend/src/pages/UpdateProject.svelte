<script>
    import { Router, Link } from "svelte-navigator";
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";

    import axios from "../healpers/axios";

    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import AddProjectMemberModal from "../components/ui/AddProjectMemberModal.svelte";

    import NavBar from "../components/NavBar.svelte";
    import MemberCard from "../components/MemberCard.svelte";

    export let user;

    let project, message, _class, showAddMemberModal;
    let showAlert = false;

    var path = window.location.pathname;
    var projectID = path.split("/")[2];

    const dispatch = createEventDispatcher();
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}`},
    };

    function openAddMemberModal() {
        showAddMemberModal = true;
    };

    onMount(async () => {
        try {
            const response = await axios.get(`project/${projectID}/`, config);
            project = await response.data.data;
        } catch (err) {
            if (err.response.status === 404 || err.response.status === 403) {
                window.location.href = "/not-found";
            }
        }
    });

    async function updateProjectFields(){
        let body = {
            "title": project.title,
            "short_description": project.short_description
        }
        try{
            const response = await axios.put(`project/${projectID}/`, body, config);
            project = response.data.data;
            showAlert = true;
            message = "Project updated successfully.";
            _class = "success";
            setTimeout(
            () => {
                showAlert = false;
            }, 3000);
        } catch (err) {
            if (err.response.status === 404 || err.response.status === 403) {
                window.location.href = "/not-found";
            }else if (err.response.status === 400) {
                showAlert = true;
                _class = "danger"
                message = err.response.data.message;
            }
        }
    }

    async function handleAddMember(event) {
        project.teams = project.teams;
        project.teams.push(event.detail.member);
    }

    async function removeMember(member){
        try {
            const response = await axios.delete(`project/${projectID}/members/${member.id}/`, config);
            const indx = project.teams.findIndex((v) => v.id === member.id);
            project.teams = project.teams;
            project.teams.splice(indx, 1);
            dispatch("message", {teams:project.teams});
        } catch (error) {
            console.log(error);
        }
            
    }
</script>


<section>
    {#if user}
        <NavBar projectView="true" {user} />
        {#if project}
            <div class="container mt-4">
                <div class="col-12 pb-4">
                    <p class="h4 mb-4">
                        Update
                        <Router>
                            <Link 
                                to={`/projects/${project.id}/`}>
                                <strong class="h4 title">{project.title}</strong>
                            </Link>
                        </Router>
                    </p>
                </div>
                <section class="section-tabs">
                    <ul class="nav nav-tabs mb-5" id="ex1" role="tablist">
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link active"
                                id="ex1-tab-1"
                                data-mdb-toggle="tab"
                                href="#ex1-tabs-1"
                                role="tab"
                                aria-controls="ex1-tabs-1"
                                aria-selected="true"
                                >Update Project fields</a
                            >
                        </li>
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link"
                                id="ex1-tab-2"
                                data-mdb-toggle="tab"
                                href="#ex1-tabs-2"
                                role="tab"
                                aria-controls="ex1-tabs-2"
                                aria-selected="false"
                                >Manage Project Members</a
                            >
                        </li>
                    </ul>
                    <div class="tab-content" id="ex1-content">
                        <div
                            class="tab-pane pb-4 fade show active"
                            id="ex1-tabs-1"
                            role="tabpanel"
                            aria-labelledby="ex1-tab-1"
                            >   
                            <Alert {message} {showAlert} {_class}/>
                            <div class="card mt-4 p-4">
                                <form>
                                    <div class="form-group mb-4">
                                        <strong><label for="content-title">Title</label></strong>
                                        <input bind:value="{project.title}" 
                                            type="text" class="form-control mt-2" id="content-title">
                                    </div>
                                    <div class="form-group pa-2 mb-4">
                                        <strong>
                                            <label for="content-title">Short Description</label>
                                        </strong>
                                        <textarea bind:value="{project.short_description}" 
                                            class="form-control mt-2" id="content-body" />
                                    </div>
                                </form>
                                <div>
                                    <button type="submit"
                                        class="btn btn-success" 
                                        on:click="{updateProjectFields}">Submit
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane pb-4 fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
                            <div class="add-member text-center mb-4">
                                <button type="button" class="btn plus-background text-light"
                                    on:click={openAddMemberModal} >
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
                            {#if project.teams && project.teams.length > 0}
                                <div class="row">
                                    {#each project.teams as member}
                                        <MemberCard {member}>
                                            <Link 
                                                to=""
                                                class="dropdown-item text-danger" 
                                                on:click="{removeMember(member)}">
                                                Remove {member.first_name}
                                            </Link>
                                        </MemberCard>
                                    {/each}
                                </div>
                            {:else}
                                <div class="col-12 text-center">
                                    <Alert 
                                        showAlert = {true} 
                                        message = {"No members found, try to add new member."} 
                                        _class = {"info"}
                                    />
                                </div>
                            {/if}
                        </div>
                    </div>
                </section>
            </div>
        {/if}
    {:else}
        <LoodingSpiner />
    {/if}
</section>

<AddProjectMemberModal
    on:message={handleAddMember}
    bind:showAddMemberModal
/>

<svelte:head>
    <title>Test-Tracker | Project Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        .nav-style {
            width: 50%;
            text-align: center;
        }
        .card {
            font-weight: 400;
            border: 0;
            -webkit-box-shadow: 0 2px 5px 0 rgb(0 0 0 / 16%), 0 2px 10px 0 rgb(0 0 0 / 12%);
            box-shadow: 0 2px 5px 0rgba(0,0,0,0.16),0 2px 10px 0rgba(0,0,0,0.12);
        }
        .testimonial-card .card-up {
            height: 120px;
            overflow: hidden;
            border-top-left-radius: 0.25rem;
            border-top-right-radius: 0.25rem;
        }
        .indigo.lighten-1 {
            background-color: #5c6bc0 !important;
        }
        .indigo {
            background-color: #3f51b5 !important;
        }
        .testimonial-card .avatar {
            width: 120px;
            height: 120px;
            margin-top: -60px;
            overflow: hidden;
            border: 5px solid #fff;
            border-radius: 50%;
            background: #5a79b1;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            font-size: 30px;
            font-weight: 600;
            color: #fff;
        }
        .testimonial-card .card-body {
            text-align: center;
        }
        .testimonial-card .avatar .avatar-span {
            width: 100%;
        }
    </style>
</svelte:head>
