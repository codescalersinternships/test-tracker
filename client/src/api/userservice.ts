import axios, { AxiosInstance } from 'axios'
import { Project } from '@/types/types'

const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNzI1ODUxLCJpYXQiOjE3MjM3MTY1NTEsImp0aSI6Ijc1NzI1NDVjNGQ3YjQ0ZGZiYzMxODIwN2RhMWRmZTdhIiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.FjfyIPg3LVDGZDkcHYjS2MRdav0Xy8TnrloJvTVTLs8',
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})

export async function postProject (project :Partial<Project>) {
  return AuthClient.post('/dashboard/projects/', project)
}

export async function getProjects (page :number) {
  return AuthClient.get('/dashboard/projects/', {
    params: {
      cursor: page,
    },
  })
}

export async function searchProject (searchInput: string) {
  await AuthClient.get(`/project/search/${searchInput}`)
}

export { AuthClient, BaseClient }
