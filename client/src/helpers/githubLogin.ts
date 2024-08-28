import axios from '../api/axios'

export async function getToken (code:any) {
  try {
    const response = await axios.BaseClient.post('/auth/github/access_token/', {
      client_id: window.env.GITHUB_CLIENT_ID,
      client_secret: window.env.GITHUB_CLIENT_SECRET,
      code,
    })
    const token = response.data.access_token
    // const refreshtoken = response.data.refresh_token
    localStorage.setItem('TEST_TRACKER_ACCESS_TOKEN', token)
    return response.data.access_tokens
    // localStorage.setItem('TEST_TRACKER_REFRESH_TOKEN', refreshtoken)
  } catch (error) {
    console.error(error)
  }
}

export async function getUser (accessToken:any) {
  try {
    const user = await axios.BaseClient.post('/auth/github/user/', {
      access_token: getToken(null),
    })
    return user.data
  } catch (error) {
    console.error(error)
  }
}
