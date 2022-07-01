export function formFields() {
    // Return form fileds based on key => Backend Model
    // We have one modal for all [post, create] request
    let path = window.location.pathname;
    let projectID = path.split("/")[2];
    let pram = path.split("/")[4]; // Thats mean there is one more param like ['projectTestPlan', 'projectTestSuite'] etc..
    let objID = Number.isInteger(parseInt(pram)) // To check if this real int number or not.

    let objectsModels = {
        "project": {
            "message": "New Project",
            "url": "/dashboard/projects/",
            "fields":{
                "title":"",
                "short_description":"",
            }
        },
    };
    if (path.includes(`/projects/${projectID}`)){
        objectsModels["test_plan"] = {
            "message": "New Test Plan",
            "url": `/test_plan/${projectID}/`,
            "fields":{
                "title":"",
                "project_id":projectID,
                "type":null,
            }
        };
        objectsModels["requirement_Doc"] = {
            "message": "New Requirement Document",
            "url": `/requirements/${projectID}/`,
            "fields":{
                "title":"",
                "project_id":projectID,
            }
        };
        objectsModels["test_suite"] = {
            "message": "New Test Suite",
            "url": `/test_suites/${projectID}/`,
            "fields":{
                "title":"",
                "project_id":projectID,
                "test_plan":"",
            }
        };
        if (objID){
            if (path.includes(`/projects/${projectID}/requirements/${pram}`)){
                objectsModels["requirement"] = {
                    "message": "New Requirement",
                    "url": `/requirements/projects/${projectID}/requirement/${pram}/`,
                    "fields":{
                        "title":"",
                        "description":"",
                        "project_id":projectID,
                        "requirement_Doc":pram,
                    }
                };
            } else if (path.includes(`/projects/${projectID}/test-plans/${pram}`)) {
                objectsModels["test_plan_content_area"] = {
                    "message": "New Test Plan Contet Area",
                    "url": `/test_plan/${projectID}/${pram}/temps/`,
                    "fields":{
                        "title":"",
                        "content":"",
                    }
                };
            } else if (path.includes(`/projects/${projectID}/test-suites/${pram}`)) {
                objectsModels["test_case"] = {
                    "message": "New Test Case",
                    "url": `/test_cases/suites/${pram}/`,
                    "fields":{
                        "title":"",
                        "description":"",
                        "test_steps":"",
                        "expected_result":"",
                        "test_suite":pram,
                        "project_id":projectID,
                    }
                };
            }
        }
        objectsModels["test_run"] = {
            "message": "New Test Run",
            "url": `/test_runs/projects/${projectID}/`,
            "fields":{
                "title":"",
                "test_plan":"",
                "test_suites":"",
                "project_id":projectID,
            }
        };
    };
    return objectsModels;
};

export function statusFields() {
    // This function is used to get all test run 
    // status to make a request to the server.
    const data = [
        {title: "Not started", id: "not started"},
        {title: "In progress", id: "in progress"},
        {title: "Completed", id: "completed"},
    ]
    return data;
};

export function runTestCaseFields(type){
    // This function will call when we need to set custom 
    // fields based on test case status => type
    const types = ["pass", "fail", "skip"];
    if (types.includes(type)){
        let body = {
            pass: {
                "passed": true,
                "failed": false,
                "skipped": false,
            },
            fail: {
                "failed": true,
                "passed": false,
                "skipped": false,
            },
            skip: {
                "skipped": true,
                "passed": false,
                "failed": false,
            },

        };
        body[type].run = true;
        body[type].completed = true;
        body[type].comments = "";
        return body[type];
    };
    return 400 // just like bad filter to make a conditional error
};