"""
Test the lambda_handler function successfully unzips multiple files and uploads their contents to S3.
"""
import os
import sys

# Add the root directory of your project to the PYTHON PATH.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import io
import zipfile

import pytest
from mock import MagicMock, patch
from extract.lambdas.unzip_s3_files import lambda_handler

def setup_mock_s3(mock_boto_client, zip_content=b''):
    """
    Helper function to set up the mock S3 client and event.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
        zip_content (bytes): Content of the zip file to be returned by the mock S3 client.

    Returns:
        tuple: A tuple containing the mock S3 client and the event dictionary.
    """
    mock_s3 = mock_boto_client.return_value
    mock_s3.get_object.return_value = {'Body': io.BytesIO(zip_content)}

    event = {
            "Records": [
                    {
                            "s3": {
                                    "bucket": {"name": "test-bucket"},
                                    "object": {"key": "test.zip"}
                            }
                    }
            ]
    }

    return mock_s3, event


@patch('boto3.client')
def test_lambda_handler_successfully_unzips_multiple_files(mock_boto_client):
    r"""
    Test the lambda_handler function successfully unzips multiple files and uploads their contents to S3.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
    """
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('file1.txt', b'content of file1')
        zip_file.writestr('file2.txt', b'content of file2')
        zip_file.writestr('file3.txt', b'content of file3')

    zip_buffer.seek(0)  # Reset the buffer position to the beginning

    mock_s3, event = setup_mock_s3(mock_boto_client, zip_content=zip_buffer.read())

    response = lambda_handler(event)

    assert response['statusCode'] == 200
    assert 'Successfully unzipped and processed files.' in response['body']
    mock_s3.put_object.assert_any_call(Bucket='test-bucket', Key='file1.txt', Body=b'content of file1')
    mock_s3.put_object.assert_any_call(Bucket='test-bucket', Key='file2.txt', Body=b'content of file2')
    mock_s3.put_object.assert_any_call(Bucket='test-bucket', Key='file3.txt', Body=b'content of file3')


@patch('boto3.client')
def test_lambda_handler_handles_empty_zip(mock_boto_client):
    r"""
    Test the lambda_handler function handles an empty zip file correctly.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
    """
    # Create an empty zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w'):
        pass  # Just create an empty zip file
    zip_buffer.seek(0)

    mock_s3, event = setup_mock_s3(mock_boto_client, zip_content=zip_buffer.read())

    response = lambda_handler(event)

    assert response['statusCode'] == 200
    assert 'Successfully unzipped and processed files.' in response['body']
    mock_s3.put_object.assert_not_called()


@patch('boto3.client')
def test_lambda_handler_handles_invalid_zip(mock_boto_client):
    r"""
    Test the lambda_handler function raises a BadZipFile exception for an invalid zip file.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
    """
    mock_s3, event = setup_mock_s3(mock_boto_client, zip_content=b'not a zip file')

    response = lambda_handler(event)

    assert response['statusCode'] == 400
    assert 'Invalid zip file' in response['body']
