# Network and Security

It is necessary to configure some `Security Groups` so that the `LambdaCaption` can comunicate with the `CaptionAPI`.

## Key Pair

Create a new `key-pair` for the project.

## IAM

* caption-api-role: Create an `IAM Role` for `EC2` with `AmazonS3FullAccess`
* backend: Create an `IAM Role` for `EC2` with `AmazonS3FullAccess` and `AmazonCognitoReadOnly`

## lambda-caption-sg

* It is not necessary to configure `Inbound` or `Outbound` rules. If you wish, after creating the `<caption-api-sg>`, come back and select on `Outbound Rules`:
  * Type: Custom TCP
  * Port range: 8080
  * Destination: `<caption-api-sg>`

## caption-api-sg

This `Security Group` is configured to allow access only from the `<lambda-caption-sg>`

* For `Inbound Rules`, choose:
  * Type: Custom TCP
  * Port range: 8080
  * Source: `<lambda-caption-sg>`

## frontend-sg

This `Security Group` is created to allow `HTTP` access from any address.

* For `Inbound Rules`, choose:
  * Type: HTTP
  * Source: Anywhere

## backend-sg

This `Security Group` is configured to allow access only from the `<frontend-sg>`

* For `Inbound Rules`, choose:
  * Type: Custom TCP
  * Port range: 8080
  * Source: Anywhere

## SES

On `Amazon SES`, verify the email that you will use to notify the users.
