<script>
    import { onMount } from "svelte";
    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte";
    import Dropdown from "../components/ui/Dropdown.svelte";
    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    let testPlansContents,
        temps,
        tempsCopy,
        projectID,
        planID,
        showDeleteModal,
        title;

    onMount(async () => {
        // Loading test plan
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        planID = path.split("/")[4];
        try {
            const responseContents = await axios.get(
                `/test_plan/${projectID}/actions/${planID}/`,
                config
            );
            testPlansContents = responseContents.data.data;
            temps = testPlansContents.temps;
            tempsCopy = temps;
        } catch (error) {
            if (error.response.status == 404) {
                window.location.href = "/not-found/";
            }
        }
    });

    async function handleSearch(event) {
        const searchContents = event.detail.objects;
        temps = searchContents;
    }

    function setContent(contentArea) {
        title = contentArea;
        showDeleteModal = true;
    }

    async function handleDelete(event) {
        const content = event.detail.obj;
        const indx = temps.findIndex((v) => v.title === content.title);
        temps = temps;
        temps.splice(indx, 1);
    }
</script>

<section>
    {#if user && testPlansContents}
        <NavBar projectView="true" 
            {user}
            on:message={
                (event) => {
                    if(event.detail.obj.data.type === "test_plan_content_area"){
                        temps = temps;
                        temps.unshift(event.detail.obj.data);
                    }
                }
            }
        />
        <div class="container pb-5">
            <div class="pt-4">
                <p class="h4 mb-2">
                    Test Plans |
                    <strong class="h4 text-primary">{testPlansContents.title}</strong>
                </p>

                <p class="text-muted">
                    {#if testPlansContents.temps}
                        There are <strong class="text-primary"
                            >{testPlansContents.temps.length}</strong
                        >
                        {testPlansContents.temps.length === 1
                            ? "area"
                            : "areas"}
                    {/if}
                </p>
            </div>
            <div class="row mt-4">
                <div class="col-6">
                    <div
                        class="card mb-3 text-center btn-primary"
                        style="font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Created : {testPlansContents.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div
                        class="card mb-3 text-center btn-primary"
                        style="font-size: 20px;font-weight: 600;"
                    >
                        <div class="card-body pb-2">
                            <p>Updated : {testPlansContents.modified}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="pt-4">
                <p>Search On TestPlans Contents</p>
                <Search
                    request="/test_plan/{projectID}/{planID}/temps/"
                    objects={temps}
                    objectsCopy={tempsCopy}
                    on:message={handleSearch}
                />
            </div>
            <div class="pt-5">
                {#if temps && temps.length}
                    {#each temps as contentArea}
                        <div class="card mb-3">
                            <div class="card-body pb-2">
                                <Dropdown>
                                    <li>
                                        <button
                                            class="dropdown-item text-danger drop-size plus-hover"
                                            on:click={setContent(
                                                contentArea
                                            )}>Delete</button
                                        >
                                    </li>
                                </Dropdown>
                                <h5 class="card-title text-primary">{contentArea.title}</h5>
                                <p class="mt-4 text-muted">
                                    {contentArea.content}
                                </p>
                            </div>
                        </div>
                    {/each}
                {:else}
                    <div class="col-12 last-projects-notfound pt-3">
                        <Alert 
                            _class={'info'} 
                            showAlert={true} 
                            message={"There are no content areas in this test plan, Try adding one."} 
                        />
                    </div>
                {/if}
            </div>
        </div>
    {/if}
    <DeleteModal
        bind:showDeleteModal
        on:message={handleDelete}
        obj={title}
        onRequest="/test_plan/{projectID}/{planID}/temps"
    />
</section>

<svelte:head>
    <title>Test-Tracker | Test Plan Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        .dropdowncustom {
            position: absolute;
            font-size: 0;
            right: 0;
            width: 35px;
        }
    </style>
</svelte:head>
