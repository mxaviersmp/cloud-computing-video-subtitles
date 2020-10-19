# Lambda Functions

These are the lambda functions responsible for generating the `Transcribe` and `Translate`
files and saving information on `DynamoDB`.

Each function needs specific `IAM` role permissions. All of these roles need to be configured for the Lambda service.
All 4 need `AWSLambdaExecute`, and use the `Python 3.8 Runtime`.
For each lambda set the necessary `Environment Variables`.

## LambdaTranscribe

* This function starts the `Amazon Transcribe` job.
* Create an execution role with the `AmazonTranscribeFullAccess` and `AmazonS3FullAccess` permissions.
* Add a trigger for `S3`, on the `<videos-bucket>`, with prefix `original` and suffix `.mp4`.
* Env variables:
  * TRANSCRIBE_BUCKET: Bucket to save the Transcribe result.

## LambdaTranslate

* This uses the `Amazon Transcribe` output and `Amazon Translate` to create the captions.
* Create an execution role with the `TranslateFullAccess` and `AmazonS3FullAccess` permissions.
* Add a trigger for `S3`, on the `<transcribe-bucket>`, with suffix `.json`.
* Since this lambda waits for the translate service to finish, increase the timeout and memory on `Basic Settings`.
* Env variables:
  * TRANSLATE_BUCKET: Bucket to save the subtitle files.

## LambdaCaption

* This function calls the `CaptionAPI`.
* Create an execution role with the `AmazonEC2FullAccess` permission.
* Add the bucket to the same `VPC` as the `CaptionAPI`.
* Choose the `<lambda-caption-sg>`
* Add a trigger for `S3`, on the `<translate-bucket>`, with prefix `pt` and suffix `.vtt`.
* Env variables:
  * VIDEO_BUCKET: Bucket with the videos.
  * TRANSLATE_BUCKET: Bucket with the subtitles.
  * CAPTION_API: Address of the `caption-api`.

## LambdaFinish

* This function saves the job information and notifies the user via email.
* Create and execution role with the `AmazonDynamoDBFullAccess`, `AmazonS3ReadOnlyAccess` and `AmazonSESFullAccess`.
* Add a trigger for `S3`, on the `<videos-bucket>`, with prefix `info` and suffix `.json`.
* Env variables:
  * VIDEOS_TABLE: Table with the videos information.
  * SOURCE_EMAIL: Email used to send the notification.
