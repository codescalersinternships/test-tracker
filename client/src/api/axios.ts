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

async function CreateNewTestSuite(testSuiteDetails: any, project_id:any){
  await AuthClient.post(`/test_suites/${project_id}/`)
  .then(response=>{
  })
  .catch(error=>{
    return error
  })
}
async function GetTestSuites(project_id:any){
  await AuthClient.get(`/test_suites/${project_id}/`)
  .then(response=>{
    return response.data
  })
  .catch(error=>{
    return error
  })
}

async function SearchSuite(project_id:any,key_word:any){
  await AuthClient.get(`/test_suites/${project_id}/search/${key_word}/`)
  .then(response=>{
    return response.data
  })
  .catch(error=>{
    return error
  })
}

export default{ AuthClient, BaseClient,GetPlans, CreateNewTestSuite, GetTestSuites,SearchSuite };
