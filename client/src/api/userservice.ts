import axios, { AxiosInstance } from 'axios'
import { UserProfile } from './../types/types'

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

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', { settings })
}

export { AuthClient, BaseClient }
