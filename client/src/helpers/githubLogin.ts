import axios from '../api/axios'

const clientId = 'Ov23lix4FAZvEzpWD76J'
const clientSecret = 'a625c62adbd77c4d1d161a40f0b7baf72c3cfacf '

export async function getToken (code:any) {
  try {
    const _getToken = await axios.BaseClient.post('/auth/github/access_token/', {
      client_id: clientId,
      client_secret: clientSecret,
      code,
    })
    console.log(_getToken)
    return _getToken.data.results.access_token
  } catch (error) {
    console.error(error)
  }
}

export async function getUser (accessToken:any) {
  try {
    console.log(accessToken)
    const user = await axios.BaseClient.post('/auth/github/user/', {
      access_token: accessToken,
    })
    return user
  } catch (error) {
    console.error(error)
  }
}
