from rest_framework import response, status, serializers
from django.core import exceptions

from tj_packages import sns_sms
from users import models


def resetPassword(request):
    data = request.data
    confirm_password = data.get("confirm_password", "")
    password = data.get("password", "")
    mobile_number = data.get("mobile_number", "")
    country_code = data.get("country_code",  "")
    otp_verification_code = data.get("otp_verification_code", "")

    if not mobile_number or not country_code:
        raise serializers.ValidationError({
            "result": False,
            "msg": "mobile_number or country_code missing or empty"}, # noqa
            code="validation_error",
        )
    if not otp_verification_code:
        raise serializers.ValidationError({
            "result": False,
            "msg": "Please enter OTP from your registered mobile number"}, # noqa
            code="validation_error",
        )
    if not str(otp_verification_code).isdigit():
        raise serializers.ValidationError({
            "result": False,
            "msg": "otp_verification_code should be only numbers"},
            code="validation_error",
        )
    try:
        user_profile_details = (
            models.UserProfileDetails.objects.select_related(
                "user").get(
                    mobile_number=mobile_number, country_code=country_code,
                    is_active=True)
        )
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
                "result": False,
                "msg": "Invalid OTP or User"
            }, code="validation_error",
        )
    user_instance = models.User.objects.get(
        id=user_profile_details.user_id)
    if user_instance.check_password(password):
        raise serializers.ValidationError({
            "result": False,
            "msg": "New password should not be same as old password"},
            code="validation_error",
        )
    existing_verfication_code = user_profile_details.otp_verification_code
    if int(existing_verfication_code) == int(otp_verification_code):
        if not password and not confirm_password:
            return response.Response({
                "result": False,
                "msg": "New password or confirm password is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if password != confirm_password:
            return response.Response(
                {"result": False, "msg": "Password mismatch"}, # noqa
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user_profile_details.user.set_password(password)
            user_profile_details.user.save()
            return response.Response(
                {
                    "result": True,
                    "msg": "Your password has been changed successfully.",
                },
                status=status.HTTP_200_OK,
            )


def password_reset_send_otp(request: object, otp_code: int):
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
        user_profile_details = models.UserProfileDetails.objects.select_related(  # noqa
            "user").get(
                mobile_number=mobile_number, country_code=country_code,
                user__is_active=True)
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
                "result": False,
                "msg": "Account does not exist for this mobile number"
            }, code="validation_error",
        )
    user_profile_details.otp_verification_code = otp_code
    user_profile_details.save()
    sns_sms.send_forgot_password_sms(
        mobile_number=user_profile_details.mobile_number,
        country_code=country_code, otp_code=otp_code)
    return response.Response({
        "result": True,
        "msg": "OTP sent to the registered mobile number",
        "data": {
            "mobile_number": user_profile_details.mobile_number,
            "country_code": user_profile_details.country_code
        }
        }, status=status.HTTP_200_OK,
    )


def password_reset_verify_otp(request: object):

    data = request.data
    mobile_number = data.get("mobile_number", "")
    country_code = data.get("country_code", "")
    otp_verification_code = data.get("otp_verification_code", 0)

    if not mobile_number or not country_code:
        raise serializers.ValidationError({
            "result": False,
            "msg": "mobile_number or country_code missing or empty"
            }, code="validation_error",
        )
    if not otp_verification_code:
        raise serializers.ValidationError({
            "result": False,
            "msg": "Please enter OTP from your registered mobile number"
            }, code="validation_error",
        )
    if not str(otp_verification_code).isdigit():
        raise serializers.ValidationError({
            "result": False,
            "msg": "otp_verification_code should be only numbers"},
            code="validation_error",
        )
    try:
        user_profile_details = (
            models.UserProfileDetails.objects.select_related(
                "user").get(
                    mobile_number=mobile_number, country_code=country_code,
                    is_active=True)
        )
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
                "result": False,
                "msg": "Invalid OTP or User"
            }, code="validation_error",
        )

    existing_verfication_code = user_profile_details.otp_verification_code
    if int(existing_verfication_code) == int(otp_verification_code):
        return response.Response({
            "result": True,
            "msg": "OTP verified successfully",
            },
            status=status.HTTP_200_OK,
        )
    else:
        return response.Response({
            "result": False,
            "msg": "Invalid OTP"
            }, status=status.HTTP_400_BAD_REQUEST,
        )
