import boto3

SERVICE_BUCKET = "ai-platform"


s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id="local_access_key",
    aws_secret_access_key="local_secret_key",
    endpoint_url="http://localhost:4566",
)
