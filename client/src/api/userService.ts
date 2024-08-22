import { UserProfile } from '../types/types'
import { AuthClient } from './clients'

export async function putSettings (settings :Partial<UserProfile>) {
  return AuthClient.put('/auth/settings/', settings)
}
