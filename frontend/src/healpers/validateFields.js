export function validateFields (data) {
    if (data.fields){
        data = data.fields
    }
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
        data[filed] = "";
        // if (!standerdFields.includes(filed)) {
        // }
    }
};
