import axios, { AxiosInstance } from 'axios'

export const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    Authorization: accessToken ? `Bearer ${accessToken}` : '',
    'Content-Type': 'application/json',
  },
})

export const BaseClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})
