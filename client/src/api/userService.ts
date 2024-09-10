import { axios } from './axios'
import { Password, UserProfile } from '../types/types'
import md5 from 'md5'

export async function putSettings (settings :Partial<UserProfile>) {
  let response: any
  try {
    response = await axios.put('/auth/settings/', settings)
  } catch (error) {
    console.error(error)
    throw error
  }
  return response
}

export async function putPassword (passwords :Partial<Password>) {
  let response: any
  try {
    response = await axios.put('/auth/change-password/', passwords)
  } catch (error) {
    console.error(error)
    throw error
  }
  localStorage.setItem('TTPHASH', md5(passwords.new_password!))
  return response
}
