import boto3
from botocore.errorfactory import UserNotFoundException

cognito = boto3.client('cognito-idp', region='us-east-1')

def verify_user(user_pool, user_id):
    try:
        cognito.admin_get_user(
            UserPoolId=user_pool,
            Username=user_id
        )
        return True
    except UserNotFoundException:
        return False

