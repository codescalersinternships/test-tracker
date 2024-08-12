import axios, { AxiosInstance } from 'axios'
import { Project } from '@/types/types'

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

export async function postProject (project :Partial<Project>) {
  console.log(project)
  return AuthClient.post('/dashboard/projects/', { project })
}

export async function searchProject (searchInput: string) {
  await AuthClient.get(`/project/search/${searchInput}`)
}

export { AuthClient, BaseClient }
