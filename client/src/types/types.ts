export type Activity = {
    action: string,
    date: string,
}

export type Project = {
    id: number,
    user: string,
    teams: string[],
    modified: string,
    created: string,
    activity: Activity[],
    // total_test_plan:
    // total_requirements_docs:
    // total_suites:
    // total_test_runs
    // incomplete_test_runs_assigned_to_you:
    // people_with_the_most_incomplete_test_runs:
    title:string,
    repo_link:string,
    short_description:string,
}
