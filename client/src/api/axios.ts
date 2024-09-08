import axiosClient from 'axios'

export const axios = axiosClient.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('TEST_TRACKER_ACCESS_TOKEN'),
  },
})
