import boto3
import botocore

from django.template.loader import render_to_string

from vid_rivals_project import constants

from django.conf import settings


def send_verification_mail(
        username: str, email_id: str, verification_url: str):
    SENDER = "<support@vidrivals.com>"
    RECIPIENT = email_id
    SUBJECT = "Verify your email address | Vid Rivals"
    BODY_TEXT = "Amazon SES"
    context = {
        "email_id": email_id,
        "username": username,
        "verification_url": verification_url,
    }
    BODY_HTML = render_to_string("send_verification_mail.html", context)
    CHARSET = "UTF-8"
    client = boto3.client(
        "ses",
        region_name=constants.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        response = client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
        )
    except botocore.exceptions.ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent! Message ID:"),
        print(response["MessageId"])
