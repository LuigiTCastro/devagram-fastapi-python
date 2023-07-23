from botocore.exceptions import ClientError
from decouple import config

import boto3
# boto3 is a lib and the official AWS SDK for python to integrate with Amazon S3 for image uploads using FastApi.



class AWSProvider:

    def s3_file_upload(self, file_path, path_to_save, bucket='devagram-python-bucket'):

        s3_client = boto3.client(
            's3',
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            aws_access_key_id=config('AWS_ACCESS_KEY_ID')
        )

        try:
            s3_client.upload_file(file_path, bucket, Key=path_to_save)

            photo_url = s3_client.generate_presigned_url(
                'get_object',
                ExpiresIn=0,
                Params={'Bucket': bucket, 'Key': path_to_save}
            )

            # return photo_url
            return str(photo_url).split('?')[0]

        except ClientError as error:
            print(error)
            return False



