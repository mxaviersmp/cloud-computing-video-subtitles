# Interface

These are the instructions to setup the user interface.

First install `quasar-cli`
```
$ yarn global add @quasar/cli
# or
$ npm install -g @quasar/cli
```

In `frontend` folder run `npm install` or `yarn` or to install all dependencies.

To initalize aplication run `quasar dev`

**Atention**

The `.env` file must to be configurated and placed at root of `frontend` folder. Shoud be like this:

```
COGNITO_USER_POOL_ID=
COGNITO_WEB_CLIENT_ID=
COGNITO_POOL_DOMAIN=
COGNITO_POOL_REDIRECT_URL=

API_BASE_URL= <backend-url>
```

## Back-end

* Install the requirements.
* Run with the command: `python back.py`.
* The code documentation explains the endpoints.
* You must add the users manually on `DynamoDB`.
