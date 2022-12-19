<script>
    import Dropdown from "../ui/Dropdown.svelte";
    import snarkdown from "snarkdown";
    import AddNewTestCase from "./AddNewTestCase.svelte";
    import Alert from "../ui/Alert.svelte";

    export let section;

    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let thisTestCase;
    let showDeleteModal;

    function setTestCase(testCase) {
        thisTestCase = testCase;
        showDeleteModal = true;
    };
</script>

{#if section.test_cases && section.test_cases.length > 0}
    <div class="row pt-4">
        {#each section.test_cases as test_case}
            <div class="col-12">
                <div class="card test_case_card">
                    <div class="card test_case_card">
                        <Dropdown>
                            <li>
                                <button
                                    class="dropdown-item text-danger drop-size plus-hover"
                                    on:click={setTestCase(test_case)}
                                    >Delete
                                </button>
                            </li>
                        </Dropdown>
                        <a
                            data-mdb-toggle="collapse"
                            href="#collapse-{test_case.id}"
                            role="button"
                            aria-expanded="false"
                            aria-controls="collapse-{test_case.id}"
                        >
                            <span class="text-primary h5">
                                {test_case.testcase_title}
                            </span>
                            <span class="text-muted h5">
                                {test_case.title}
                            </span>
                        </a>

                        <div class="test_case_info">
                            <a
                                class="collapse_span"
                                data-mdb-toggle="collapse"
                                href="#collapse-{test_case.id}"
                                role="button"
                                aria-expanded="false"
                                aria-controls="collapse-{test_case.id}"
                            >

                            </a>
                            <div class="row" style="margin-left: 10px;">
                                <div class="col-3">
                                    <small>Updated on</small>
                                </div>
                                <div class="col-3">
                                    <small>Last saved by</small>
                                </div>
                                <div class="col-6">
                                    <small>Associated requirements</small>
                                </div>

                                <div class="col-3">
                                    <strong
                                        ><small>{test_case.modified}</small
                                        ></strong
                                    >
                                </div>
                                <div class="col-3">
                                    <strong
                                        ><small>
                                            <a
                                                style="font-size: 15px;"
                                                class="text-primary"
                                                href="/members/{test_case
                                                    .last_saved.id}"
                                                >@{test_case.last_saved
                                                    .full_name}</a
                                            >
                                        </small></strong
                                    >
                                </div>
                                {#if test_case.requirement}
                                    <div class="col-6">
                                        <a href="/projects/{projectID}/requirements/{test_case.requirement.requirement_doc}">
                                            <strong>
                                                <small>
                                                    {test_case.requirement
                                                    .requirement_title}-{test_case
                                                    .requirement.title}
                                                </small>
                                            </strong>
                                        </a>
                                    </div>
                                {:else}
                                    <div class="col-6">
                                        <small>No associated requirement</small>
                                    </div>
                                {/if}
                            </div>
                            <div
                                class="collapse collapse-style"
                                id="collapse-{test_case.id}"
                            >
                                <small>Description:</small><br />
                                <p>{test_case.description}</p>
                                <small>Test steps:</small><br />
                                {@html snarkdown(test_case.test_steps)}
                                <small>Expected result</small><br />
                                {@html snarkdown(test_case.expected_result)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/each}
        <AddNewTestCase testCases={section.test_cases}/>
    </div>
{:else}
    <div class="col-12">
        <Alert 
            showAlert = {true} 
            message = {"There are no test cases yet, try to create one"} 
            _class = {"info"}
        />
    </div>
{/if}