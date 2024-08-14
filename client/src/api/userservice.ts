import axios, { AxiosInstance } from 'axios'
import { UserProfile } from './../types/types'

const AuthClient: AxiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // import.meta.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNjQ0ODA2LCJpYXQiOjE3MjM2MzU1MDYsImp0aSI6ImY1MWJmZTIxZmFlOTQ1OWM5ZjIyODQwMDFlMWQ2MzM2IiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.0tTLb8pOwWcyRCPU1nn8ugY1JDGGmOcr9E7VVZzDpMw', // localStorage.getItem('token'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  // baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', { settings })
}

export { AuthClient, BaseClient }
