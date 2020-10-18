import api from './api'

const list = async (userid) => {
  const { data: response } = await api.get(`/list?id=${userid}`)
  return response
}

const send = async (data) => {
  const { data: response } = await api.post('/send', data, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
  return response
}

export default {
  list,
  send
}
