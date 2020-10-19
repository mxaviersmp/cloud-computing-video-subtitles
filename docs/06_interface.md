# Interface

These are the instructions to setup the user interface.

First install `quasar-cli`

```txt
$ yarn global add @quasar/cli
# or
$ npm install -g @quasar/cli
```

In `frontend` folder run `npm install` or `yarn` or to install all dependencies.

To initialize the application run `quasar dev`

**__Attention__**: The `.env` file must to be configured and placed at root of `frontend` folder. Should be like this:

```txt
COGNITO_USER_POOL_ID=Id of the Cognito User Pool
COGNITO_WEB_CLIENT_ID=Id of the Cognito App Client
COGNITO_POOL_DOMAIN=Domain of the Cognito User Pool
COGNITO_POOL_REDIRECT_URL=Where to redirect after Cognito actions.
API_BASE_URL=Address of the backend.
```

## Back-end

The code documentation explains the endpoints.

* Create an `EC2` instance.
  * Select `Amazon Linux 2 AMI`.
  * Choose `t2.micro`.
  * Choose a `VPC`.
  * Choose the `<backend-role>` `IAM role`.
  * If you want to setup the machine on boot, on `Advanced Details`, paste or upload the [installation script](../backend/ec2_user_data_amazonlinux.sh) in the `User Data field.
  * Choose the `<backend-sg>` security group.
  * Choose the `<project-key-pair>`

If you didn't setup the `User Data`, login to the machine, and follow the steps on the [installation script](../backend/ec2_user_data_amazonlinux.sh).

### Env variables

* VIDEOS_BUCKET: Bucket to save the video.
* VIDEOS_TABLE: Table to save video information.
* FLASK_HOST: Address of process in machine, can set as `0.0.0.0`
* FLASK_PORT: Port to run the process, set as `8080`
* USER_POOL_ID: Id of the `Cognito User Pool`
