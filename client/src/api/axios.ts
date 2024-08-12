import axios, { AxiosInstance } from 'axios';

const AuthClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT, 
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem("token"),
  },
});

const BaseClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT,
  timeout: 1000,
});


async function GetPlans(projectId:any){
  await AuthClient.get(`/test_plan/${projectId}/`)
  .then(response=>{
    return response.data
  })
  .catch(error=>{
    return error
  })
}

async function SearchPlans(project_id:any,key_word:any){
  await AuthClient.post(`/test_plan/${project_id}/search/${key_word}/`)
  .then(response=>{
    return response.data
  })
  .catch(error=>{
    return error
  })
}

export default{ AuthClient, BaseClient,GetPlans,SearchPlans };
