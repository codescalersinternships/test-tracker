<script>
    import axios from '../healpers/axios';
    import Button from "./ui/Button.svelte";
    import ProjectCard from "../components/ProjectCard.svelte";

    let projects = [];
    let inputValue;

    async function searchProjects(){
        projects = []
        const projectName = document.getElementById("search-id").value;
        inputValue = projectName

        const config = {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        };

        if(projectName.length > 0){
            const response = await axios.get(
                `/project/search/${projectName}/`,config
            )
            if (response.data.data.length > 0) {
                projects = response.data.data
            }
    
            if (projects.length > 0) {
                document.querySelector('.last-projects').style.display = 'none';
                document.querySelector('.search-result').style.display = 'block';
                document.querySelector('.no-result').style.display = 'none';
            } else {
                document.querySelector('.last-projects').style.display = 'none';
                document.querySelector('.search-result').style.display = 'none';
                document.querySelector('.no-result').style.display = 'block';
            }
        } else {
            document.querySelector('.no-result').style.display = 'none';
            document.querySelector('.search-result').style.display = 'none';
            document.querySelector('.last-projects').style.display = 'block';
        }

    }
</script>



<section>
    <div class="pt-4">
        <p>
            Search projects:
        </p>
        <div class="input-group">
            <input id="search-id" type="search" class="form-control rounded" placeholder="Search"
            aria-label="Search" aria-describedby="search-addon" />
            <Button Class="btn btn-outline-primary" Function={searchProjects} text="Search" />
        </div>
        <div class="pt-5 search-result" style="display: none">
            <p>Search Result</p>
            <div class="row p-1">
                {#each projects as project}
                    {#if project.name.length > 25}
                        <ProjectCard title={project.name.slice(0,25)+'..'} date={project.created} link={`/projects/project_id=${project.id}`}/>
                    {:else}
                        <ProjectCard title={project.name} date={project.created} link={`/projects/project_id=${project.id}`}/>
                    {/if}
                {/each}
            </div>
        </div>
        <div class="col-12 no-result pt-3" style="display: none;">
            <p class="text-muted">
                -- There are no projects with name {inputValue}
            </p>
        </div>
    </div>
</section>