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
    total_test_plan: any,
    total_requirements_docs: any,
    total_suites: any, // update the any to type of each attribute
    total_test_runs: any,
    incomplete_test_runs_assigned_to_you: any,
    people_with_the_most_incomplete_test_runs: any,
    title:string,
    repo_link:string,
    short_description:string,
}
