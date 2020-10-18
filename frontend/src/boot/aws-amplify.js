require('dotenv').config()

import Amplify from '@aws-amplify/core'
import Auth from '@aws-amplify/auth'

Amplify.configure({
  aws_cognito_region: 'us-east-1',
  aws_user_pools_id: process.env.COGNITO_USER_POOL_ID,
  aws_user_pools_web_client_id: process.env.COGNITO_WEB_CLIENT_ID,
  oauth: {
    domain: process.env.COGNITO_POOL_DOMAIN,
    scope: ['phone', 'email', 'openid', 'profile', 'aws.cognito.signin.user.admin'],
    redirectSignIn: process.env.COGNITO_POOL_REDIRECT_URL,
    redirectSignOut: process.env.COGNITO_POOL_REDIRECT_URL,
    responseType: 'code'
  },
  federationTarget: 'COGNITO_USER_POOLS'
})

export default ({ app }) => {
  app.amplify = Amplify
}

export { Amplify, Auth }
