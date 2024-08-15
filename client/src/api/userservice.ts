import axios, { AxiosInstance } from 'axios'
import { UserProfile } from './../types/types'

const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNzEwOTAxLCJpYXQiOjE3MjM3MDE2MDEsImp0aSI6ImQwMzVkNzQxMDRkZjQ2YWZhMDEzNTQ4MDlmMDU1ZWNlIiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.79uxdN3zeLO5uLPGLlzynWHjpZ1mYm3VF11s_QaeFIQ', // localStorage.getItem('token'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', settings)
}

export { AuthClient, BaseClient }
