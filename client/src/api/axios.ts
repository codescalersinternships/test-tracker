import axiosClient from 'axios'

const accessToken = localStorage.getItem('TESTTRACKER_ACCESS_TOKEN')
export const axios = axiosClient.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
})

async function search (searchInput:any) {
  try {
    return await axios.get(`/members/search/${searchInput}`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function addMember (inviteNewMember:any) {
  try {
    await axios.post(`/dashboard/members/`, inviteNewMember)
  } catch (error) {
    console.error(error)
    throw error
  }
}
async function getMembers () {
  try {
    return await axios.get(`/api/members/all/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { search, getMembers, addMember }
