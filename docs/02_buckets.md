# S3 Buckets

The project uses 3 buckets.

## videos-bucket

* This bucket will store the uploaded and captioned videos.
* Create the folders: `original`, `info` and `captioned`.
* In `Permissions -> Block Public Access`, leave only the first 2 options selected.
* Paste the following `policy`on the `Permissions -> Bucket Policy` to allow the captioned videos to be downloaded by the users.
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicRead",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::<videos-bucket>/captioned/*"
            }
        ]
    }
    ```

## transcribe-bucket

* This bucket will store the `Amazon Transcribe` output.

## translate-bucket

* This bucket will store the files used to caption the videos.
* Create the folders: `en` and `pt`.
