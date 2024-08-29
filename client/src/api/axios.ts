import axiosClient from 'axios'

const accessToken = localStorage.getItem('TESTTRACKER_ACCESS_TOKEN')
export const axios = axiosClient.create({
  baseURL: 'https://server.gent02.dev.grid.tf',
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
})
