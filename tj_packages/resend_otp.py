from rest_framework import serializers, response, status
from django.core import exceptions
from vid_rivals_app import models as vidrivals_models

from users import models
from tj_packages import sns_sms


def resend_otp(request: object, otp_code: int, subject: str, message: str):
    data = request.data
    mobile_number = data.get("mobile_number", "")
    country_code = data.get("country_code", "")

    if not mobile_number or not country_code:
        return response.Response({
            "result": False,
            "msg": "mobile_number or country_code missing or empty" # noqa
            }, status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user_profile_details = (
            models.UserProfileDetails.objects.select_related(
                "user").get(
                    mobile_number=mobile_number, country_code=country_code)
        )
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
                "result": False,
                "msg": "Invalid User to resend OTP"
            }, code="validation_error",
        )

    if user_profile_details.otp_verified is True:
        return response.Response({
            "result": True,
            "msg": "OTP Already Verified for this account"
            }, status=status.HTTP_200_OK,
        )

    user_profile_details.otp_verification_code = otp_code
    user_profile_details.save()
    vidrivals_models.SmsTracker.objects.create(
            subject=subject, message=message, mobile_number=mobile_number)
    sns_sms.send_sms(
        mobile_number=mobile_number, country_code=country_code,
        subject=subject, message=message)
    return response.Response({
        "result": True,
        "msg": "OTP sent to the registered mobile number"
        }, status=status.HTTP_200_OK,
    )
