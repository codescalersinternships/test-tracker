import { Password, UserProfile } from '../types/types'
import { AuthClient } from './axios'

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', settings)
}

export async function putPassword (passwords :Partial<Password>) {
  return AuthClient.put('/auth/change-password/', passwords)
}
