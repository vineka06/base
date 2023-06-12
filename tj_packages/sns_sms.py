import boto3
import random

from django.conf import settings


def send_sms(
        mobile_number: str, country_code: str, subject: str, message: str):
    mobile_number_country_code = str(country_code) + str(mobile_number)
    client = boto3.client(
        "sns",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1"
    )

    client.publish(
        PhoneNumber=mobile_number_country_code,
        Subject=subject,
        Message=message
    )


def send_forgot_password_sms(
        mobile_number: int, country_code: str, otp_code: int):
    mobile_number_country_code = str(country_code) + str(mobile_number)
    client = boto3.client(
        "sns",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1"
    )

    client.publish(
        PhoneNumber=mobile_number_country_code,
        Subject="Vidrivals",
        Message=f"Your verification code for Vid Rivals reset password is {otp_code}" # noqa
    )


def generate_otp():
    return random.randint(1000, 9999)
