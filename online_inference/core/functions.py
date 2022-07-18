import boto3
from core.credetials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def get_file_from_s3(filename, bucket='made'):
    s3 = boto3.resource('s3', endpoint_url='https://storage.yandexcloud.net', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    object = s3.Object(bucket, filename)
    with open('tmp/' + filename, 'wb') as data:
        object.download_fileobj(data)
