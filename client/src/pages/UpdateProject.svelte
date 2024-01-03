<script>
    import { Router, Link } from "svelte-navigator";
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";

    import axios from "../healpers/axios";

    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import Input from "../components/ui/Input.svelte";
    import TextArea from "../components/ui/TextArea.svelte";
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
            project = await response.data.results
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
            project = response.data.results
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
                                <strong class="h4 text-primary">{project.title}</strong>
                            </Link>
                        </Router>
                    </p>
                </div>
                <section class="section-tabs">
                    <ul class="nav nav-tabs mb-5" id="ex1" role="tablist">
                        <li class="nav-item nav-style" role="presentation">
                            <a
                                class="nav-link active nav-link-tab"
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
                                class="nav-link nav-link-tab"
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
                                <Input
                                    title={"Title."}
                                    type={"text"}
                                    id={"p-title"}
                                    bind:value={project.title}
                                />
                                <TextArea 
                                    title="Short Description"
                                    bind:value="{project.short_description}"
                                />
                                <div>
                                    <button type="submit"
                                        class="btn btn-primary" 
                                        on:click="{updateProjectFields}">Submit
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane pb-4 fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
                            <div class="add-member text-center mb-4">
                                <button type="button" class="btn btn-primary width-100 text-light"
                                    on:click={openAddMemberModal} >
                                    <i class="fas fa-plus" style="font-size: 25px;"></i>
                                </button>
                            </div>
                            {#if project.teams && project.teams.length > 0}
                                <div class="row">
                                    {#each project.teams as member}
                                        <MemberCard {member}>
                                            <Link 
                                                to=""
                                                class="dropdown-item text-danger drop-size plus-hover" 
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
        .nav-style {
            width: 50%;
            text-align: center;
        }
    </style>
</svelte:head>
