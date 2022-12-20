<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    import { addNewCaseToSuite } from "../../healpers/api";
    import Alert from "../ui/Alert.svelte";
    import Loadingbtn from "../ui/Loadingbtn.svelte";
    import LoodingSpiner from "../ui/LoodingSpiner.svelte";

    export let projectID;
    export let section;
    export let testSuite;

    const dispatch = createEventDispatcher();

    let path = window.location.pathname;
    let testSuiteID = path.split("/")[4];

    let testCases = [];
    let isLoading = false;
    let isLoadingBtn = false;

    onMount(async () => {
        if (section.test_cases == null || section.test_cases == undefined){
            section.test_cases = []
        };
        /** @type {Set<number>} */
        const caseSet = new Set(section.test_cases.map(({ id }) => id));
        testCases = testSuite.test_cases.filter(({ id }) => !caseSet.has(id));
    });
</script>

{#if isLoading}
    <LoodingSpiner />
{:else if testCases.length > 0}
    <small class="text-muted text-center mb-4">
        If a test case doesn't already exist in this test suite, then the
        existing test case will be linked, else an identical copy will be
        created.
    </small>

    <div class="card cases-card">
        <div class="card-header">
            <div class="row">
                <div class="col-6">Test case title</div>
                <div class="col-3 text-center">Linked suites</div>
                <div class="col-3 text-center">-</div>
            </div>
        </div>
    </div>

    <div class="card cases-card over-scroll mb-4">
        <div class="card-header case-content">
            <div class="row">
                {#each testCases as tcase}
                    {#if !section.test_cases.includes(tcase)}
                        <div class="col-12 mb-3 cases-lines">
                            <div class="row">
                                <div class="col-6">
                                    {tcase.testcase_title}-{tcase.title}
                                </div>
                                <div class="col-3 text-center">
                                    {testSuiteID}
                                </div>
                                <div class="col-3 text-center">
                                    <button
                                        class="btn new-section-button"
                                        disabled={isLoadingBtn}
                                        on:click={async () => {
                                            isLoadingBtn = true;
                                            const added = await addNewCaseToSuite(
                                                projectID,
                                                section.id,
                                                tcase.id
                                            );
                                            if (added) {
                                                dispatch("message", {
                                                    obj: added,
                                                });
                                            }
                                            isLoadingBtn = false;
                                        }}
                                    >
                                        {#if isLoadingBtn}
                                            <Loadingbtn />
                                        {:else}
                                            Add Case
                                        {/if}
                                    </button>
                                </div>
                            </div>
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
    </div>

{:else}
    <Alert
        showAlert={true}
        message={"There are no test cases available in this test suite, try to create a new one by selecting `New` instead of `Existing`"}
        _class={"primary"}
    />
{/if}
