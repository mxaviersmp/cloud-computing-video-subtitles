# CaptionAPI

The `CaptionAPI` performs the union of the video with it's captions.

## Instance Configuration

* Create an `EC2` instance.
  * Select `Amazon Linux 2 AMI`.
  * Choose `t2.medium`.
  * Choose a `VPC`.
  * Choose the `<caption-api-role>` `IAM role`.
  * If you want to setup the machine on boot, on `Advanced Details`, paste or upload the `ec2_user_data_amazonlinux.sh` in the `User Data field.
  * Choose `Storage Size` of `30 GB`.
  * Choose the `<caption-api-sg>` security group.
  * Choose the `<project-key-pair>`

If you didn't setup the `User Data`, login to the machine, and follow the steps on the `ec2_user_data_amazonlinux.sh` file.
