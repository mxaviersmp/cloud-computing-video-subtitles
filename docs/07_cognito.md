# Cognito

## Cognito Configuration

* Select `Manage User Pools` option
  * Create a user poll
  * Set a name for the user pool and choose `Review defaults`
  * In the left menu choose option `Attributes`
    * Select option `Email address or phone number`
    * In `Which standard attributes do you want to require?` Choose fields `name` and `email`
    * click in next step

  * In next page, uncheck all requires for password
    * Require numbers
    * Require special character
    * Require uppercase letters
    * Require lowercase letters

    * click in `next step`

  * In `MFA and Verifications` don't change anything and click in `next step`

  * In `Messages customization` set the `Verification type` to `Link` and be free to write a Email subject and Email Message like you want. This message will be send to user after signup for confirm email. Click in `next step`

  * In `tags` and `devices` don change anything.

  * In appClient click in `add an app client`
    * Set a name
    * Uncheck `Generate client secret` **Important**
    * Click in `create app client`
  * In `Triggers` do nothing and click in `save changes`
  * Now click in `Create pool`

## How to get .env values

* COGNITO_USER_POOL_ID
  * The first value in tab general settings

* COGNITO_WEB_CLIENT_ID
  * In `General settings` > `App clients`

* COGNITO_POOL_DOMAIN
  * Go to `App integration` menu option
  * Click in `add domain`
  * Choose a domain name and save
  * Back to `App integration` the url will be there

* COGNITO_POOL_REDIRECT_URL
  * `In app integration` > `App client settings`
  * set the url to be called after signin and signout
    * for localhost `https://localhost:8080` in both.
