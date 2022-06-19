export function validateFields (data) {
    for (const filed in data.fields) {
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
    const standerdFields = ["project_id", "requirement_Doc", "requirement"];
    for (const filed in data.fields) {
        if (!standerdFields.includes(filed)) {
            data.fields[filed] = "";
        }
    }
};
