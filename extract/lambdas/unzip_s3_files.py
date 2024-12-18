"""
This module contains an AWS Lambda function to unzip files stored in an S3 bucket.
"""

import io
import zipfile

import boto3


def lambda_handler(event):
    """
    AWS Lambda function to unzip files stored in an S3 bucket.

    Parameters:
    event (dict): Event data passed by AWS Lambda, containing S3 bucket and object key information.

    Returns:
    dict: A dictionary containing the status code, and a success message.
    """
    s3 = boto3.client("s3")
    bucket = None  # Initialize bucket variable

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Download the zip file from S3
        zip_obj = s3.get_object(Bucket=bucket, Key=key)
        buffer = io.BytesIO(zip_obj["Body"].read())

        # Unzip the file, and upload its contents back to S3
        with zipfile.ZipFile(buffer) as zip_ref:
            for file in zip_ref.namelist():
                s3.put_object(Bucket=bucket, Key="{}".format(file), Body=zip_ref.read(file))

    return {"statusCode": 200, "body": "Successfully unzipped files in {}".format(bucket)}
