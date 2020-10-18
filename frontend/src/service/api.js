import axios from 'axios'

const api = axios.create({
  baseURL: process.env.API_BASE_URL || 'http://0.0.0.0:5000'
})

export default api
