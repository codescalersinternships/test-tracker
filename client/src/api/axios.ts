import axios, { AxiosInstance } from 'axios'
import md5 from 'md5'
const AuthClient: AxiosInstance = axios.create({
  baseURL: 'https://server.gent02.dev.grid.tf/api',
  headers: {
    'Content-Type': 'application/json',
    Authorization: 'Bearer ' + localStorage.getItem('token'),
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
    localStorage.setItem('token', token)
    localStorage.setItem('password', md5(userInfo.password))
  } catch (error:any) {
    localStorage.removeItem('token')
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
// function md5 (password: any): string {
//   throw new Error('Function not implemented.')
// }
