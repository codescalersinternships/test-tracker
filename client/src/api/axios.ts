import axios, { AxiosInstance } from 'axios'

const AuthClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('token'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  timeout: 1000,
})

async function GetPlans (projectId:string) {
  try {
    localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNzI0Njg5LCJpYXQiOjE3MjM3MTUzODksImp0aSI6IjlmNTU1NmY0MjQzZTRjMmI5OWZmZTcxYjFkNWQxYmJiIiwidXNlcl9pZCI6MSwiZW1haWwiOiJuYWJpbGFAZ21haWwuY29tIn0.OUIvvLV5sgtyVQM_PtLu4HsqJaeOLC5FIx7w39VZ7js')
    await AuthClient.get(`/test_plan/${projectId}`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function SearchPlans (projectId:any, keyWord:any) {
  try {
    return await AuthClient.post(`/test_plan/${projectId}/search/${keyWord}/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function DeletePlan (projectId:any, testPlanId:any) {
  try {
    await AuthClient.delete(`/test_plan/${projectId}/actions/${testPlanId}/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function UpdatePlanTitle (projectId:any, testPlanId:any, title:any) {
  try {
    await AuthClient.put(`/test_plan/${projectId}/${testPlanId}/update/`, title)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { AuthClient, BaseClient, GetPlans, SearchPlans, DeletePlan, UpdatePlanTitle }
