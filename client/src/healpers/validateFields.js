export function validateFields (data) {
    if (data.fields){
        data = data.fields
    }
    const standerdFields = ["project_id", "requirement_Doc", "requirement", "test_suite", "repo_link"];
    for (const filed in data) {
        if (filed === "repo_link" && data["repo_link"] === "" && data["github_repo"] === true){
            return false;
        };
    
        if (data[filed] === "" && !standerdFields.includes(filed)
        ) {
            return false;
        }
    }
    return true;
};

export function claerFields (data) {
    if (data.fields){
        data = data.fields
    };

    const standerdFields = ["project_id", "requirement_Doc", "requirement", "test_suite"];
    
    for (const filed in data) {
        
        if (!standerdFields.includes(filed)){
            if (data[filed] === true || data[filed] === false){
                data[filed] = false;
            } else {
                data[filed] = "";
            };
        };
    };
};

export function validateEmail(email) {
    return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}