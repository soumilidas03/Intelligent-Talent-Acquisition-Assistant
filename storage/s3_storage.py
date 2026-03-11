import boto3
import os
import io
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def upload_resume(file_bytes, filename):

    try:

        file_obj = io.BytesIO(file_bytes)

        s3.upload_fileobj(file_obj, BUCKET_NAME, filename)

        url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{filename}"

        return url

    except Exception as e:
        print("S3 Upload Error:", e)
        return None