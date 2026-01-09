import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
bucket = os.environ['BUCKET_NAME']
prefix = 'uploads/'

def lambda_handler(event, context):
    try:
        if event['rawPath'] == '/upload':
            return handle_upload(event)
        elif event['rawPath'].startswith('/files/'):
            return handle_download(event)
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def handle_upload(event):
    body = json.loads(event.get('body', '{}'))
    filename = body.get('filename')
    content_type = body.get('content_type', 'application/octet-stream')

    if not filename:
        return {'statusCode': 400, 'body': json.dumps({'error': 'filename required'})}

    object_key = prefix + str(uuid.uuid4()) + '_' + filename

    url = s3.generate_presigned_url('put_object',
                                    Params={'Bucket': bucket,
                                            'Key': object_key,
                                            'ContentType': content_type},
                                    ExpiresIn=900)  # 15 minutes

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'object_key': object_key, 'upload_url': url})
    }

def handle_download(event):
    object_key = event['pathParameters']['objectKey']

    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': bucket, 'Key': object_key},
                                    ExpiresIn=3600)  # 1 hour

    return {
        'statusCode': 307,
        'headers': {'Location': url}
    }
