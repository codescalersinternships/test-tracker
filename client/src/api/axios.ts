import axiosClient from 'axios'
import md5 from 'md5'

const accessToken = localStorage.getItem('TESTTRACKER_ACCESS_TOKEN')
export const axios = axiosClient.create({
  baseURL: window.env.SERVER_DOMAIN_NAME_API,
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
})
async function SignUp (newUser:any) {
  try {
    await axios.post('/auth/signup/', newUser)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function SignUpInvitation (passwords:any) {
  try {
    await axios.put('/members/set_password/', passwords)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function LogInUser (userInfo:any) {
  try {
    const response = await axios.post('/auth/login/', userInfo)
    const token = response.data.access_token
    const refreshtoken = response.data.refresh_token
    localStorage.setItem('TEST_TRACKER_ACCESS_TOKEN', token)
    localStorage.setItem('TTPHASH', md5(userInfo.password))
    localStorage.setItem('TEST_TRACKER_REFRESH_TOKEN', refreshtoken)
  } catch (error:any) {
    localStorage.removeItem('TEST_TRACKER_ACCESS_TOKEN')
    throw new Error(error)
  }
}

async function LogInGitHub () {
  try {
    return await axios.post('/auth/github/access_token/')
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { LogInUser, LogInGitHub, SignUp, SignUpInvitation }
