export function validateFields (data) {
    if (data.fields){
        data = data.fields
    }
    for (const filed in data) {
        if (data[filed] === "" 
            || data[filed] === undefined
            || data[filed] === null
        ) {
            return false;
        }
    }
    return true;
};

export function claerFields (data) {
    const standerdFields = ["project_id", "requirement_Doc", "requirement", "test_suite"];
    for (const filed in data.fields) {
        if (!standerdFields.includes(filed)) {
            data.fields[filed] = "";
        }
    }
};
