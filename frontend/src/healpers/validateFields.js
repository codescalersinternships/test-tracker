export function validateFields (data) {
    for (const filed in data.fields) {
        console.log(filed, data.fields[filed]);
        if (data.fields[filed] === "" 
            || data.fields[filed] === undefined
            || data.fields[filed] === null
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
