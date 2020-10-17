import api from './api'

const get = async (data) => {
  const { data: response } = await api.get('/list', data)
  return response
}

const send = async (data) => {
  const { data: response } = await api.post('/send', data)
  return response
}

export default {
  get,
  send
}
