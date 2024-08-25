import axios, { AxiosInstance } from 'axios'

const AuthClient: AxiosInstance = axios.create({
  baseURL: window.location.origin,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('token'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: window.location.origin,
  timeout: 1000,
})

async function search (searchInput:any) {
  try {
    return await AuthClient.get(`/members/search/${searchInput}`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function addMember (inviteNewMember:any) {
  try {
    await AuthClient.post(`/dashboard/members/`, inviteNewMember)
  } catch (error) {
    console.error(error)
    throw error
  }
}
async function getMembers () {
  try {
    return await AuthClient.get(`/api/members/all/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { AuthClient, BaseClient, search, getMembers, addMember }
