import axios, { AxiosInstance } from 'axios'

export const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: localStorage.getItem('token'),
  },
})

export const BaseClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})
