import { axios } from './axios'
import { inviteNewMember } from '../types/types'

async function search (searchInput:string) {
  try {
    return await axios.get(`/members/search/${searchInput}`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function addMember (inviteNewMember:inviteNewMember) {
  try {
    await axios.post(`/dashboard/members/`, inviteNewMember)
  } catch (error) {
    console.error(error)
    throw error
  }
}
async function getMembers () {
  try {
    localStorage.setItem('TESTTRACKER_ACCESS_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0OTM2NTM5LCJpYXQiOjE3MjQ5MjcyMzksImp0aSI6IjgwMDY5OTAzZDNjMzRjMzVhMzdjMWZmMjc3ZWMxMWQ0IiwidXNlcl9pZCI6MSwiZW1haWwiOiJuYWJpbGFAZ21haWwuY29tIn0.NWT-fAt4vCyefqDeCRRLqnG2q2sDBQJq7jrRRSmgcK4')
    return await axios.get(`/api/members/all/`)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { search, getMembers, addMember }
