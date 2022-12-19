<script>
    import { onMount } from "svelte";
    import axios from "../../healpers/axios";

    let path = window.location.pathname;
    let testSuiteID = path.split("/")[4];

    let testCases = [];
    let isLoading = false;
    
    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    onMount(async () => {
        isLoading = true;
        const response = await axios.get(`test_cases/test_suite/${testSuiteID}/`, config);
        testCases = response.data.data;
        console.log(testCases);
    });
</script>


{#if testCases}
    <small class="text-muted text-center mb-4">
        If a test case doesn't already exist in this test suite, then the existing test case will be linked, else an identical copy will be created.
    </small>
    <div class="card cases-card">
        <div class="card-header">
            <div class="row">
                <div class="col-6">
                    Test case title
                </div>
                <div class="col-3 text-center">
                    Linked suites
                </div>
                <div class="col-3 text-center">
                    -
                </div>
            </div>
        </div>
    </div>
    {#each testCases as tcase }
        <div class="card cases-card over-scroll mb-4">
            <div class="card-header case-content">
                <div class="row">
                    <div class="col-6">
                        {tcase.testcase_title}-{tcase.title}
                    </div>
                    <div class="col-3 text-center">
                        {testSuiteID}
                    </div>
                    <div class="col-3 text-center">
                        <button class="btn new-section-button" >
                            Add Case
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/each}
{/if}
