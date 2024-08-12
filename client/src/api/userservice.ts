import axios, { AxiosInstance } from 'axios'
import { Project } from '@/types/types'

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyODUzNjM3LCJpYXQiOjE3MjI4NDQzMzcsImp0aSI6ImE3ODgxOGRlZWMxNjRlYjFhYjFkMGVkNDliNzFmMWZjIiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.-7sAr7ny0arkuLywbrqkJquo3rSo82DubitVXRb0zp0'
localStorage.setItem('token', token)

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

export async function postProject (project :Project) {
  return AuthClient.post('/dashboard/projects/', { project })
}

export async function searchProject (searchInput: string) {
  await AuthClient.get(`/project/search/${searchInput}`)
}

export { AuthClient, BaseClient }
