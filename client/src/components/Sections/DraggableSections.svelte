<script>
    import {flip} from 'svelte/animate';
    import TestCasesSections from "./TestCasesSections.svelte"
    import Alert from "../ui/Alert.svelte";
    
    export let list = [];
    export let testSuite;
  
    let hovering = false;
  
    const drop = (event, target) => {
      event.dataTransfer.dropEffect = 'move'; 
      const start = parseInt(event.dataTransfer.getData("text/plain"));
      const newTracklist = list
  
      if (start < target) {
        newTracklist.splice(target + 1, 0, newTracklist[start]);
        newTracklist.splice(start, 1);
      } else {
        newTracklist.splice(target, 0, newTracklist[start]);
        newTracklist.splice(start + 1, 1);
      }
      list = newTracklist
      hovering = null
    }
  
    const dragstart = (event, i) => {
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.dropEffect = 'move';
      const start = i;
      event.dataTransfer.setData('text/plain', start);
    }
  
</script>

{#if list.length > 0}
  <div class="row pt-4">
    {#each list as section, index  (section.id)}
      <div class="col-12 list-item" animate:flip draggable={true} 
        on:dragstart={event => dragstart(event, index)}
        on:drop|preventDefault={event => drop(event, index)}
        ondragover="return false"
        on:dragenter={() => hovering = index}
        class:is-active={hovering === index}>
        <div class="card test_case_card">
          <a data-mdb-toggle="collapse" href="#collapse-{section.id}" role="button"
            aria-expanded="false" aria-controls="collapse-{section.id}">
            <span class="text-primary h5">
              {section.title}
            </span>
          </a>
          <div class="test_case_info">
            <a class="collapse_span" data-mdb-toggle="collapse" href="#collapse-{section.id}"
              role="button" aria-expanded="false" aria-controls="collapse-{section.id}">
              <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30"
                fill="currentColor" class="bi bi-chevron-compact-down" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1.553 6.776a.5.5 0 0 1 .67-.223L8 9.44l5.776-2.888a.5.5 0 1 1 .448.894l-6 3a.5.5 0 0 1-.448 0l-6-3a.5.5 0 0 1-.223-.67z"/>
              </svg>
            </a>
            <div class="collapse collapse-style" id="collapse-{section.id}">
                <TestCasesSections {testSuite} {section} />
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
{:else}
  <Alert 
    message={"There are no sections created in this test suite, try to create a new one."}
    showAlert={true}
    _class={"info mt-4"}
    />
{/if}