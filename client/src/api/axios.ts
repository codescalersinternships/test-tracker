import axiosClient from 'axios'

export const axios = axiosClient.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NzkzNDY0LCJpYXQiOjE3MjU3ODQxNjQsImp0aSI6ImI0Nzk5NTE3NmJlODQ5NDRhODA2MmI5NTUxYWI4OWNmIiwidXNlcl9pZCI6NSwiZW1haWwiOiJib3VkaWUyMDAzQGdtYWlsLmNvbSJ9.LG02kVuoHWFycqcVtATITE6qe7LYvaGHUgwjWm8OqYo',
  },
})
