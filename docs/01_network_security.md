# Network and Security

It is necessary to configure some `Security Groups` so that the `LambdaCaption` can comunicate with the `CaptionAPI`.

## Key Pair

Create a new `key-pair` for the project.

## VPC

Create a new `VPC` for the project.

## lambda-caption-sg

* Choose the `project-vpc`.
* **__Note:__** It is not necessary to configure `Inbound` or `Outbound` rules. If you wish, after creating the `<caption-api-sg>`, come back and select on `Outbound Rules`:
  * Type: Custom TCP
  * Port range: 8080
  * Destination: <caption-api-sg>

## caption-api-sg

This `Security Group` is configured to allow access only from the `<lambda-caption-sg>`

* Choose the `project-vpc`.
* For `Inbound Rules`, choose:
  * Type: Custom TCP
  * Port range: 8080
  * Destination: `<lambda-caption-sg>`

## SES

On `Amazon SES`, verify the email that you will use to notify the users.
