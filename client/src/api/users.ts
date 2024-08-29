import { axios } from './axios'
import md5 from 'md5'

async function signUp (newUser:any) {
  try {
    await axios.post('/auth/signup/', newUser)
  } catch (error) {
    console.error(error)
    throw error
  }
}

async function signUpInvitation (passwords:any) {
  try {
    await axios.put('/members/set_password/', passwords)
  } catch (error) {
    console.error(error)
    throw error
  }
}

export async function logInUser (userInfo: any): Promise<void> {
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

export default { logInUser, signUp, signUpInvitation }
