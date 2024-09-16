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

export async function login (userInfo: Partial<UserProfile>) {
  try {
    const response = await axios.post('/auth/login/', userInfo)

    localStorage.setItem('TEST_TRACKER_ACCESS_TOKEN', response.data.access_token)
    localStorage.setItem('TTEHASH', response.data.email)
    localStorage.setItem('TTPHASH', md5(userInfo.password!))
    localStorage.setItem('TEST_TRACKER_REFRESH_TOKEN', response.data.refresh_token)
  } catch (error) {
    localStorage.removeItem('TEST_TRACKER_ACCESS_TOKEN')
    localStorage.removeItem('TTEHASH')
    localStorage.removeItem('TTPHASH')
    localStorage.removeItem('TEST_TRACKER_REFRESH_TOKEN')

    console.error(error)
    throw error
  }
}

export async function logout () {

}
