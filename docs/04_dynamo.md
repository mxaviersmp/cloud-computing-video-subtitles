# DynamoDB

You will need 2 tables, one for the users and one for the videos.
The only configuration needed is to create the tables with the keys, as the attributes will be created as needed.

## users-table

* Set the `Primary key` as `user_id`
* A user with all atributes will have the following:
    ```txt
    {
        user_id: str
        username: str
        email: str
    }
    ```

## videos-table

* Set the `Primary key` as `video_id`
* A video with all atributes will have the following:
    ```txt
    {
        video_id: str
        video_name: str
        user_id: str
        finished: bool
        duration: float
        transcription_words: float
        translation_words: float
    }
    ```
