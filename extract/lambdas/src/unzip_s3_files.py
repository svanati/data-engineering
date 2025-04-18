"""
This module contains an AWS Lambda function to unzip files stored in an S3 bucket.
"""

import io
import zipfile

import boto3
from botocore.exceptions import ClientError


def lambda_handler(event):
    """
    AWS Lambda function to unzip files stored in an S3 bucket.

    Parameters:
    event (dict): Event data passed by AWS Lambda, containing S3 bucket and object key information.

    Returns:
    dict: A dictionary containing the status code, and a success message.
    """
    try:
        # Check if the event contains records
        if "Records" not in event or not event["Records"]:
            return {"statusCode": 400, "body": "Event does not contain any records."}

        # Extract bucket name and key from the event
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]

        # Initialize S3 client
        s3_client = boto3.client("s3")

        # Get the zip src from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        if "Body" not in response:
            raise Exception("Missing Body in S3 response")
        zip_content = response["Body"].read()

        # Unzip the src
        with zipfile.ZipFile(io.BytesIO(zip_content), "r") as zip_ref:
            for file_name in zip_ref.namelist():
                # Extract src content in memory
                with zip_ref.open(file_name) as file:
                    file_content = file.read()

                    # Upload each src to the same S3 bucket
                    s3_client.put_object(
                        Bucket=bucket_name, Key=file_name, Body=file_content
                    )

        return {"statusCode": 200, "body": "Successfully unzipped and processed files."}

    except KeyError as e:
        return {"statusCode": 400, "body": f"Missing key in event data: {str(e)}"}
    except ClientError as e:
        return {"statusCode": 500, "body": f"Error interacting with S3: {str(e)}"}
    except zipfile.BadZipFile as e:
        return {"statusCode": 400, "body": f"Invalid zip file: {str(e)}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An unexpected error occurred: {str(e)}"}
