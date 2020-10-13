import api from './api'

const get = async (userId) => {
  const { data } = await api.get(`/users/${userId}/work`)
  return data
}

const save = async (work) => {
  const { data } = await api.post(`/users/${work.userId}/work`, work)
  return data
}

const deleteWork = async (work) => {
  const data = await api.delete(`/users/${work.id}/work`)
  return data
}

const update = async (work) => {
  const data = await api.put(`/users/${work.id}/work`, work)
  return data
}

export default {
  get,
  save,
  deleteWork,
  update
}
