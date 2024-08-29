import axiosClient from 'axios'

const accessToken = localStorage.getItem('TESTTRACKER_ACCESS_TOKEN')
export const axios = axiosClient.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  headers: {
    Authorization: accessToken ? `Bearer ${accessToken}` : '',
  },
})
