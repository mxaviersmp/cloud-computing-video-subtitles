import axios from 'axios'
import authService from './authService'

const getAccessToken = async () => {
  const session = await authService.getSession()
  if (session) {
    const { token } = session
    return token
  }
  return ''
}

const api = axios.create({
  baseURL: process.env.API_BASE_URL || 'http://localhost:3333'
})

api.interceptors.request.use(async (request) => {
  const token = await getAccessToken()
  request.headers.authorization = `Bearer ${token}`
  return request
})

export default api
