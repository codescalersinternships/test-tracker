import axiosClient from 'axios'

const accessToken = localStorage.getItem('TESTTRACKER_ACCESS_TOKEN')
export const axios = axiosClient.create({

  // window.env.SERVER_DOMAIN_NAME_API
  baseURL: 'https://server.gent02.dev.grid.tf',
  headers: {
    Authorization: accessToken ? `Bearer ${accessToken}` : '',
  },
})
