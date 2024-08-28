import axios, { AxiosInstance } from 'axios'
import md5 from 'md5'
const AuthClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('TEST_TRACKER_ACCESS_TOKEN'),
  },
})

const BaseClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
})

async function SignUp (newUser:any) {
  try {
    await BaseClient.post('/auth/signup/', newUser)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function SignUpInvitation (passwords:any) {
  try {
    await BaseClient.put('/members/set_password/', passwords)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function LogInUser (userInfo:any) {
  try {
    const response = await BaseClient.post('/auth/login/', userInfo)
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
    return await BaseClient.post('/auth/github/access_token/')
  } catch (error) {
    console.error(error)
    throw error
  }
}

export default { AuthClient, BaseClient, LogInUser, LogInGitHub, SignUp, SignUpInvitation }
