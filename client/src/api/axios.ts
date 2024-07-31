import axios, { AxiosInstance } from 'axios'
import { ProfileSettings } from './../types/types'

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyMjU4MDU1LCJpYXQiOjE3MjIyNDg3NTUsImp0aSI6Ijg3MDZhZGE2MzRmNTQ2NTFiZGZlNzI2NTYxOGQyNDJkIiwidXNlcl9pZCI6MSwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.dW1qlBMJgumrScdKTuLaKDAZqo8YjzggErn-w4Da1rM'
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

export async function putSettings (settings :ProfileSettings) {
  // await this.refresh_token()
  return AuthClient.put('/auth/settings/', { settings })
}

export { AuthClient, BaseClient }
