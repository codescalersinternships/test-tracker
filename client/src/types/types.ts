enum Status {
    NOT_STARTED='not_started',
    IN_PROGRESS='in_progress',
    COMPLETED='completed',
}

export type Activity = {
    action: string,
    date: string,
}

export type TestPlan = {
    id: number,
    modified: string,
    created: string,
    title: string,
    type: string,
}

export type Requirement = {
    id: number,
    updated: string,
    created: string,
    title: string,
    requirements: string[],
}

export type TestSuite = {
    id: number,
    modified: string,
    created: string,
    title: string,
    number_of_test_cases: number,
    test_plan: number,
}

export type TestRun = {

}

export type TestCase = {
    id: number,
    modified: string,
    created: string,
    title: string,
    testcase_title: string,
    requirement: string
    last_saved: {
        id: number,
        full_name: string,
    }
    test_suite: string,
    description: string,
    test_steps: string,
    expected_result: string,
}
export type Project = {
    id: number,
    user: string,
    teams: string[],
    modified: string,
    created: string,
    activity: Activity[],
    total_test_plan: TestPlan[],
    total_requirements_docs: Requirement[],
    total_suites: TestSuite[],
    total_test_runs: TestRun[],
    incomplete_test_runs_assigned_to_you: TestRun[],
    people_with_the_most_incomplete_test_runs: TestRun[],
    title: string,
    repo_link: string,
    short_description: string,
}
