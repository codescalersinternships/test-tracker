import { axios } from './axios'
import md5 from 'md5'
import { Password, UserProfile } from '../types/types'

export async function putSettings (settings :Partial<UserProfile>) {
  return axios.put('/auth/settings/', settings)
}

export async function putPassword (passwords :Partial<Password>) {
  localStorage.setItem('TTPHASH', md5(passwords.new_password))
  return axios.put('/auth/change-password/', passwords)
}
