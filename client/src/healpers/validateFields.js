export function validateFields (data) {
    if (data.fields){
        data = data.fields
    }
    const standerdFields = ["project_id", "requirement_Doc", "requirement", "test_suite"];
    for (const filed in data) {
        if (data[filed] === "" 
            // || data[filed] === undefined
            // || data[filed] === null
        ) {
            return false;
        }
    }
    return true;
};

export function claerFields (data) {
    if (data.fields){
        data = data.fields
    }
    const standerdFields = ["project_id", "requirement_Doc", "requirement", "test_suite"];
    for (const filed in data) {
        if (!standerdFields.includes(filed)){
            
        }
        data[filed] = "";
        // if (!standerdFields.includes(filed)) {
        // }
    }
    console.log(data)
};

export function validateEmail(email) {
    return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
}