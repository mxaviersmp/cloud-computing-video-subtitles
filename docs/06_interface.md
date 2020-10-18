# Interface

These are the instructions to setup the user interface.

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
