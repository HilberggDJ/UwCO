import os
import html
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT_URL", "http://localstack:4566"),
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    name = (params.get("imie") or "").strip()

    if not name:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": "Brak parametru imie. Uzyj adresu URL z ?imie=Ola"
        }

    response = s3.get_object(
        Bucket=os.environ["TEMPLATE_BUCKET"],
        Key=os.environ.get("TEMPLATE_KEY", "template.html")
    )
    template = response["Body"].read().decode("utf-8")
    page = template.replace("{{IMIE}}", html.escape(name))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": page
    }
