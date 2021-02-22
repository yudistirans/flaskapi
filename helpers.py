import boto3, botocore
from instance.config import S3_ACCESS_KEY, S3_SECRET_ACCESS_KEY, S3_BUCKET_NAME, S3_LOCATION

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_ACCESS_KEY,
   aws_secret_access_key=S3_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file, bucket_name, upload_folder, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            upload_folder+file.filename,
            ExtraArgs={
                # "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(S3_LOCATION+upload_folder, file.filename)

def remove_file_from_s3(file, bucket_name, upload_folder):
    key = upload_folder+file
    try:
        s3.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        print("Something Happened: ", e)
        return e