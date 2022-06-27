import axios from './axios';
import { claerFields, validateFields } from './validateFields'

let config = {
    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
};

export async function postNewObject(e, data) {
    try {
        if (data.obj === "test_case"){
            if (data.fields.requirement){
                data.url = `/test_cases/suites/${data.fields.test_suite}/?requirement=${data.fields.requirement}`;
            }
        }
        if (!validateFields(data)){
            return {class:"danger", message:"Please fill all fields"};
        } else {
            const response = await axios.post(
                data.url, data.fields, config
            );
            claerFields(data);
            return {class:"success", message:response.data.message, data: response.data.data};
        }
    } catch (err) {
        if (err.response) {
            return {class:"danger", message:err.response.data.message};
        } else {
            return {class:"danger", message:err};
        }
    };
};