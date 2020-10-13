// import api from './api'
import Amplify, { Auth } from 'aws-amplify'

Amplify.configure({
  aws_cognito_region: process.env.region,
  aws_user_pools_id: process.env.POOL_ID,
  aws_user_pools_web_client_id: process.env.CLIENT_ID
})

const getSession = async () => {
  const session = await JSON.parse(localStorage.getItem('session'))
  return session
}

const getCurrentUser = async () => {
  const session = await getSession()
  return session.user
}

const signIn = async (userInfo) => {
  const { username, password } = userInfo
  try {
    const user = await Auth.signIn(username, password)
    return user
  } catch (error) {
    console.log('error signing in', error)
    throw error
  }
}

const signOut = async () => {
  try {
    await Auth.signOut()
  } catch (error) {
    console.log('error signing out: ', error)
    throw error
  }
}

const signUp = async (userInfo) => {
  const { username, password, name } = userInfo
  try {
    const { user } = await Auth.signUp({
      username,
      password,
      attributes: {
        name
      }
    })
    console.log(user)
  } catch (error) {
    console.log('error signing up:', error)
    throw error
  }
}

export default {
  getSession,
  getCurrentUser,
  signIn,
  signOut,
  signUp
}
