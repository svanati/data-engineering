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


def setup_mock_s3(mock_boto_client):
    """
    Helper function to set up the mock S3 client and event.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.

    Returns:
        tuple: A tuple containing the mock S3 client and the event dictionary.
    """
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    mock_s3.get_object.return_value = {'Body': io.BytesIO(b'fake zip content')}
    event = {"Records": [{"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "test.zip"}}}]}
    return mock_s3, event

@patch('boto3.client')
def test_lambda_handler_successfully_unzips_multiple_files(mock_boto_client):
    r"""
    Test the lambda_handler function successfully unzips multiple files and uploads their contents to S3.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
    """
    mock_s3, event = setup_mock_s3(mock_boto_client)

    with patch('zipfile.ZipFile') as mock_zipfile:
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        mock_zip.namelist.return_value = ['file1.txt', 'file2.txt', 'file3.txt']
        mock_zip.read.side_effect = [b'content of file1', b'content of file2', b'content of file3']

        response = lambda_handler(event)

        assert response['statusCode'] == 200
        assert 'Successfully unzipped files in test-bucket' in response['body']
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
    mock_s3, event = setup_mock_s3(mock_boto_client)

    with patch('zipfile.ZipFile') as mock_zipfile:
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        mock_zip.namelist.return_value = []

        response = lambda_handler(event)

        assert response['statusCode'] == 200
        assert 'Successfully unzipped files in test-bucket' in response['body']
        mock_s3.put_object.assert_not_called()

@patch('boto3.client')
def test_lambda_handler_handles_invalid_zip(mock_boto_client):
    r"""
    Test the lambda_handler function raises a BadZipFile exception for an invalid zip file.

    Args:
        mock_boto_client (MagicMock): Mocked boto3 client.
    """
    mock_s3, event = setup_mock_s3(mock_boto_client)
    mock_s3.get_object.return_value = {'Body': io.BytesIO(b'not a zip file')}

    with pytest.raises(zipfile.BadZipFile):
        lambda_handler(event)
