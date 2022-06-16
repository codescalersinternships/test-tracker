<script>
    import NavBarDropdown from './NavBarDropdown.svelte'
    import CreateNewObjModal from './CreateNewObjModal.svelte'

    let data;
    let objectsModels = {
            "project": {
                "message": "New Project",
                "url": "/dashboard/projects/",
                "fields":{
                    "title":"",
                    "short_description":"",
                }
            },
            "test_plan": {
                "message": "New Test Plan",
                "url": "/test_plan/",
                "fields":{
                    "title":"",
                    "project_id":"",
                    "type":"",
                }
            },
            "requirement_Doc": {
                "message": "New Requirement Document",
                "url": "/requirements/",
                "fields":{
                    "title":"",
                    "project_id":"",
                }
            },
            "requirement": {
                "message": "New Requirement",
                "url": "/requirements/",
                "fields":{
                    "title":"",
                    "description":"",
                    "project_id":"",
                    "requirement_Doc":"",
                }
            },
            "test_suite": {
                "message": "New Test Suite",
                "url": "/test_suites/",
                "fields":{
                    "title":"",
                    "project_id":"",
                    "test_plan":"",
                }
            },
            "test_case": {
                "message": "New Test Case",
                "url": "/test_cases/",
                "fields":{
                    "title":"",
                    "description":"",
                    "test_steps":"",
                    "expected_result":"",
                    "requirement_id":"",
                    "test_suite":"",
                }
            },
            "test_run": {
                "message": "New Test Run",
                "url": "/test_runs/",
                "fields":{
                    "title":"",
                    "test_plan":"",
                    "status":"",
                    "project_id":"",
                }
            },
        }

        function createNewObj(key) {
            data = objectsModels[key];
            data['showPostModal'] = true;
            data['obj'] = key;
        }
</script>

<div class="d-flex align-items-center">
    <NavBarDropdown>
        <span slot="dropdown-toggle" 
            class="user_photo_nav add-obj">
            <i class="fas fa-plus"></i>
        </span>
        <span slot="dropdown-li">
            {#each Object.entries(objectsModels) as [key, value]}
                <li>
                    <button class="dropdown-item"
                        style="color: #bf4e62;"
                        on:click={() => createNewObj(key)}>
                        {value.message}
                    </button>
                </li>
            {/each}
        </span>
    </NavBarDropdown>
    {#if data}
        <CreateNewObjModal data={data} />
    {/if}
</div>