import axios from "./axios";


let config = {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
};

export async function loadLast5ProjectsUpdated(){
    const responseProjects = await axios.get(
        "/project/last-5-projects/",
        config
    );
    return await responseProjects.data.data;
}

export async function loadLast5ProjectsActivity(){
    const responseActivity = await axios.get(
        "/project/last-5-projects/activity/",
        config
    );
    return await responseActivity.data.data;
}

export async function loadTestSuiteBasedOnProjectID(projectID){
    if(projectID != undefined || projectID != null){
        try {
            const responseSuites = await axios.get(
                `/test_suites/${projectID}/`,
                config
            );
            return await responseSuites.data.data;
        } catch (err) {
            return false;
        }
    }
}

export async function loadTestPlanBasedOnProjectID(projectID){
    if(projectID != undefined || projectID != null){
        try {
            const responsePlans = await axios.get(
                `/test_plan/${projectID}/`,
                config
            );
            return responsePlans.data.data;
        } catch (err) {
            return false;
        }
    }
}

export async function loadProjectRequirementsBasedOnProjectID(projectID){
    if(projectID != undefined || projectID != null){
        try {
            const responsePlans = await axios.get(
                `/test_cases/project/${projectID}/requirements/`,
                config
            );
            return responsePlans.data.data;
        } catch (err) {
            return false;
        }
    }
}