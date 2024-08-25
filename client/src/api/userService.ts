import { UserProfile } from '../types/types'
import { AuthClient } from './axios'

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', settings)
}
