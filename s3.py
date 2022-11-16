import logging
import boto3
from botocore.exceptions import ClientError
import requests
import os

def upload_file(bucket_name, folder, file_name, file_path):
    response  = create_presigned_post(bucket_name, folder+'/'+file_name)
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
    
    #Remove every .mp4 file
    for file in os.listdir():
        if file.endswith(".mp4"):
            os.remove(file) 
    #os.remove(file_path)
    
    #os.remove(filename_audio)
    print("Uploaded video")
    print(http_response.status_code)
    return

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', os.environ.get("AWS_ACCESS_KEY"), os.environ.get("AWS_SECRET_KEY"))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        #Replace expiration in string
        
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3', os.environ.get("AWS_ACCESS_KEY"), os.environ.get("AWS_SECRET_KEY"))
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response

if __name__ == "__main__":
    # Set these values before running the program
    bucket_name = 'touchlydata'
    object_name = 'dog.png'

    # Generate a presigned URL for the S3 object
    #url = create_presigned_url(bucket_name, object_name)
    response  = create_presigned_post(bucket_name, 'Output/'+object_name)
    
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
        # If successful, returns HTTP status code 204
        logging.info(f'File upload HTTP status code: {http_response.status_code}')