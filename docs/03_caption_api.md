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

## Auto Scaling and Load Balancing

You can setup and `Auto Scaling` group to run tha `API`.

* Create a new `Launch Template`. Follow the same steps as the Instance Configuration, but use the `User Data` option.
* Enable `Load Balancing`
* Create a new `Target Group`:
  * Target type: Instances
  * Protocol: TCP
  * Port: 8080
  * VPC: `<project-vpc>`
  * Don't register any targets.
* Select `Group size` at your choosing. Leave `Minimum capacity` at least 1.
* Choose `Target tracking scaling policy` and `Average CPU utilization`.
