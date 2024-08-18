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

async function Search (searchInput:any) {
  return await AuthClient.get(`/members/search/${searchInput}`)
}
async function getProjectMembers (projectId:any) {
  return await AuthClient.get(`/members/project/${projectId}/members/`)
}
export default { AuthClient, BaseClient, Search }
