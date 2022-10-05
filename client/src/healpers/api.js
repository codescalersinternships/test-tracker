import axios from "./axios";
import { validateEmail, validateFields} from "./validateFields";


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

export async function loadProjects(){
    const responseProjects = await axios.get(
        "/dashboard/projects/",
        config
    );
    return await responseProjects.data.data;
}

export async function inviteNewMember(data){
    if (!validateFields(data)){
        return {class:"danger", message:"Please fill all fields"};
    }
    if (!validateEmail(data.email)){
        return {class:"danger", message:"Please enter a valid email address."};
    }
    else {
        const response = await axios.post(
            "/dashboard/members/", data, config
        );
        return {class:"success", message:response.data.message, data: response.data.data};
    }
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