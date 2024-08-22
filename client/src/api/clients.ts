import axios, { AxiosInstance } from 'axios'

export const AuthClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzOTk0NzQ5LCJpYXQiOjE3MjM5ODU0NDksImp0aSI6ImRjMWRjMDU1ZTgzZjQ0NGQ4NDU1NTAwMGMyNDUwMTJhIiwidXNlcl9pZCI6NCwiZW1haWwiOiJib3VkaWVAYm91ZGllLmNvbSJ9.OgeODfFg5GxP1QxAAyu2FFlOMx2suAdWvjBtkK5eT0U',
  },
})

export const BaseClient: AxiosInstance = axios.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
})
