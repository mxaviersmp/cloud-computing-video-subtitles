# Lambda Function

These are the lambda functions responsible for generating the `Transcribe` and `Translate`
files and saving information on `DynamoDB`.

The `Lambda` functions are associated with 3 `buckets`.

Each function needs specific `IAM` role permissions.
All 4 need `AWSLambdaExecute`.

* `lambda_transcribe` needs `AmazonTranscribeFullAccess`
* `lambda_translate` needs `TranslateFullAccess`
* `lambda_finish` needs `AmazonDynamoDBFullAccess`, `AmazonS3ReadOnlyAccess` and `AmazonSESFullAccess`
