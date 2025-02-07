import boto3
from botocore.exceptions import NoCredentialsError
import os
from datetime import datetime
from io import BytesIO
import botocore.exceptions
from fastapi import FastAPI, UploadFile, File
from config.settings import Settings


settings = Settings()

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESSKEY,
    aws_secret_access_key=settings.AWS_SECRETEKEY,
    region_name=settings.AWS_REGIONS,
)

def generate_s3_key(filename: str) -> str:
    """Generate a partitioned S3 path (year/month/filename)."""
    current_date = datetime.utcnow()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    return f"images/{year}/{month}/{filename}"  # S3 path

def upload_to_s3(file_obj, s3_key: str):
    """Function to upload file to S3 with error handling."""
    try:
        s3_client.upload_fileobj(file_obj, settings.S3_BUCKET_NAME, s3_key)
        return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGIONS}.amazonaws.com/{s3_key}"
    except Exception as e:
        raise Exception(f"Error uploading image to S3: {str(e)}")


