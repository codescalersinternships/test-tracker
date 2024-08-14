import axios, { AxiosInstance } from 'axios'
import { UserProfile } from './../types/types'

const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNjQ2NTY5LCJpYXQiOjE3MjM2MzcyNjksImp0aSI6ImZiOTI3MGI2NjFmMzRhZmFiNzVlZTBlZjdiMzRhNzUzIiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.GOW5K_gXlW2VxkQ7Hd7rnFBm4mDfd55VctxX81FLS_I', // localStorage.getItem('token'),
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
