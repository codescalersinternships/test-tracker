<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios';
    import NavBar from "../components/NavBar.svelte";
    import Search from "../components/Search.svelte";
    import Alert from "../components/ui/Alert.svelte";
    import DeleteModal from "../components/ui/DeleteModal.svelte"


    export let user;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
    };

    let testPlansContents, temps, tempsCopy, projectID, planID, title, oldTitle, errorMessage;
    let show = false;

    onMount(async () => {
        // Loading test plan
        let path = window.location.pathname;
        projectID = path.split("/")[2];
        planID = path.split("/")[4];
        try {
            const responseContents = await axios.get(`/test_plan/${projectID}/actions/${planID}/`, config);
            testPlansContents = responseContents.data.data;
            temps = testPlansContents.temps;
            tempsCopy = temps;
        } catch (error) {
            if (error.response.status == 404) {
                window.location.href = '/not-found/'
            }
            
        }
    });

    async function handleSearch(event) {
        const searchContents = event.detail.objects;
        temps = searchContents;
    }

    function setContent(contentArea) {
        title = contentArea
        show = true;
    }

    async function handleDelete(event) {
        const content = event.detail.obj;
        const indx = temps.findIndex(v => v.title === content.title);
        temps = temps;
        temps.splice(indx, 1);
    }

    async function updateContentArea(newTitle, newBody){
        // Update test plan content area
        const data = {title:newTitle['title'], content:newBody['body']};
        try {
            const response = await axios.put(
                `/test_plan/${projectID}/${planID}/temps/${oldTitle}/`,
                data,config
            )
            document.querySelector('.update-content-modal').style.display = 'none'
            const indx = temps.findIndex(v => v.title === oldTitle);
            temps[indx] = data    
        } catch (error) {
            if (error.response.status === 400){
                document.querySelector('.alert').style.display = 'block';
                errorMessage = error.response.data.message;
                setTimeout(function() {
                    document.querySelector('.alert').style.display = 'none';
                }, 3000);
            }
        }
    }

</script>

<svelte:head>
    <title>Test-Tracker | Test Plan Detail</title>
</svelte:head>

<section>
    {#if user && testPlansContents}
        <NavBar projectView="true" user={user}/>
        <Alert message={errorMessage}/>

        <div class="container pb-5">
            <div class="pt-4">
                <p class="h5">
                    {testPlansContents.title}
                </p>
                <p class="text-muted">
                    {#if testPlansContents.temps}
                        There are <strong>{testPlansContents.temps.length}</strong> {testPlansContents.temps.length === 1 ? 'area' : 'areas'}
                    {/if}
                </p>
            </div>
            <div class="row mt-4">
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Created : {testPlansContents.created}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card mb-3 text-center" style="background: rgb(138 180 228);color: #fff;font-size: 20px;font-weight: 600;">
                        <div class="card-body pb-2">
                            <p>Updated : {testPlansContents.modified}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="pt-4">
                <p>
                    Search On TestPlans Contents
                </p>
                <Search request="/test_plan/{projectID}/{planID}/temps/" objects={temps} 
                    config={config} objectsCopy={tempsCopy} on:message={handleSearch}/>
            </div>
            <div class="pt-5">
                {#if temps}
                    {#each temps as contentArea }
                        <div class="card mb-3">
                            <div class="card-body pb-2">
                                <div class="dropdown p-1" style="position: absolute;font-size: 0;right: 0;width: 35px;">
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
                                        <!-- <li>
                                            <button on:click={setTitleAndBody(contentArea.title, contentArea.content)} 
                                                class="dropdown-item text-black">Update</button>
                                        </li> -->
                                        <li>
                                            <button class="dropdown-item text-danger" on:click={setContent(contentArea)}>Delete</button>
                                        </li>
                                    </ul>
                                </div>
                                <h5 class="card-title">{contentArea.title}</h5>
                                <p class="mt-4 text-muted">{contentArea.content}</p>
                            </div>
                        </div>
                    {/each}
                {:else}
                    <div class="col-12 last-projects-notfound pt-3">
                        <p class="text-muted">
                            -- There are no content areas in this test plan
                        </p>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
    <!-- <ModalUpdate updateFunctionOnClick={updateContentArea} title={title} body={body}/> -->
    <DeleteModal
        bind:show
        on:message={handleDelete}
        obj={title}
        onRequest='/test_plan/{projectID}/{planID}/temps'
        config={config}
    />
</section>