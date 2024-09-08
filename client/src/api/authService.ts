import { axios } from './axios'
import md5 from 'md5'
import { UserProfile } from '../types/types'

export async function signUp (newUser: Partial<UserProfile>) {
  try {
    await axios.post('/auth/signup/', newUser)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export async function signUpInvitation (password:string) {
  try {
    await axios.put('/members/set_password/', password)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export async function logInUser (userInfo: Partial<UserProfile>) {
  try {
    const response = await axios.post('/auth/login/', userInfo)
    const token = response.data.access_token
    const refreshtoken = response.data.refresh_token
    localStorage.setItem('TEST_TRACKER_ACCESS_TOKEN', token)
    localStorage.setItem('TTPHASH', md5(userInfo.password!))
    localStorage.setItem('TEST_TRACKER_REFRESH_TOKEN', refreshtoken)
  } catch (error) {
    localStorage.removeItem('TEST_TRACKER_ACCESS_TOKEN')
    throw error
  }
}
