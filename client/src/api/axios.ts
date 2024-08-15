import axios, { AxiosInstance } from 'axios';

const AuthClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api', 
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem("token"),
  },
});

const BaseClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  timeout: 1000,
});


async function GetPlans(projectId:string){
  localStorage.setItem("token","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNzI0Njg5LCJpYXQiOjE3MjM3MTUzODksImp0aSI6IjlmNTU1NmY0MjQzZTRjMmI5OWZmZTcxYjFkNWQxYmJiIiwidXNlcl9pZCI6MSwiZW1haWwiOiJuYWJpbGFAZ21haWwuY29tIn0.OUIvvLV5sgtyVQM_PtLu4HsqJaeOLC5FIx7w39VZ7js");
  await AuthClient.get(`/test_plan/${projectId}`)
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

async function DeletePlan(project_id:any,test_plan_id:any) {
  await AuthClient.delete(`/test_plan/${project_id}/actions/${test_plan_id}/`)
  .then(response=>{
  })
  .catch(error=>{
    return error
  })
}

async function UpdatePlanTitle(project_id:any,test_plan_id:any,title:any) {
  await AuthClient.put(`/test_plan/${project_id}/${test_plan_id}/update/`,title)
  .then(response=>{
  })
  .catch(error=>{
    return error
  })
}

export default{ AuthClient, BaseClient,GetPlans,SearchPlans,DeletePlan,UpdatePlanTitle };
