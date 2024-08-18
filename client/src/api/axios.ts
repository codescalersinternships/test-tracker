import axios, { AxiosInstance } from 'axios'

const AuthClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('token'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT,
  timeout: 1000,
})

async function GetPlans (projectId:any) {
  try {
    await AuthClient.get(`/test_plan/${projectId}/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function CreateNewTestSuite (testSuiteDetails: any, projectId:any) {
  try {
    await AuthClient.post(`/test_suites/${projectId}/`, testSuiteDetails)
  } catch (error) {
    console.error(error)
    throw error
  }
}
async function GetTestSuites (projectId:any) {
  try {
    return await AuthClient.get(`/test_suites/${projectId}/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function SearchSuite (projectId:any, keyWord:any) {
  try {
    await AuthClient.get(`/test_suites/${projectId}/search/${keyWord}/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { AuthClient, BaseClient, GetPlans, CreateNewTestSuite, GetTestSuites, SearchSuite }
