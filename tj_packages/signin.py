from rest_framework import serializers, response, status
from django.contrib import auth
from django.core import exceptions

from tj_packages import user_login, user_token
from users import models

User = auth.get_user_model()


def sign_in(request: object, is_active=True):

    device_id = request.META.get("HTTP_DEVICE", "")
    if str(device_id) == "":
        raise serializers.ValidationError(
            {"result": False, "msg": "device missing in Header or Invalid"},
            code="validation_error",
        )

    platform = request.META.get("HTTP_PLATFORM", "")
    if str(platform) == "":
        raise serializers.ValidationError(
            {"result": False, "msg": "Platform missing in Header or Invalid"},
            code="validation_error",
        )

    ip_address = (
        request.META.get(
            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")
        ).split(",")[0].strip()
    )

    data = request.data
    country_code = data.get("country_code", "")
    mobile_number = data.get("mobile_number", "")
    password = data.get("password", "")

    if not mobile_number or not password:
        raise serializers.ValidationError({
            "result": False,
            "msg": "mobile_number or password missing or empty"},
            code="validation_error",
        )
    try:
        user_profile = models.UserProfileDetails.objects.select_related(
            "user").get(
                mobile_number=mobile_number, country_code=country_code,
                user__is_active=is_active)
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
            "result": False,
            "msg": "Account does not exist for this mobile number"},
            code="validation_error",
        )

    is_pass = user_profile.user.check_password(password)
    if not is_pass:
        raise serializers.ValidationError({
            "result": False,
            "msg": "Invalid password"},
            code="validation_error",
        )
    else:
        user_login.update_user_login_details(
            user=user_profile.user, device_id=device_id,
            platform=platform, ip_address=ip_address)
        token = user_token.get_token(user=user_profile.user)

        if user_profile.profile_pic:
            profile_pic = user_profile.profile_pic.url
        else:
            profile_pic = ""

        if user_profile.medium_profile_pic:
            medium_profile_pic = user_profile.medium_profile_pic.url
        else:
            medium_profile_pic = ""

        if user_profile.thumbnail_profile_pic:
            thumbnail_profile_pic = user_profile.thumbnail_profile_pic.url
        else:
            thumbnail_profile_pic = ""

        return response.Response({
            "result": True,
            "msg": "success",
            "data": {
                "user_id": user_profile.user.pk,
                "token": token.key,
                "username": user_profile.user.username,
                "mobile_number": user_profile.mobile_number,
                "country_code": user_profile.country_code,
                "first_name": user_profile.user.first_name,
                "last_name": user_profile.user.last_name,
                "email": user_profile.user.email,
                "bio": user_profile.bio,
                "profile_pic": profile_pic,
                "medium_profile_pic": medium_profile_pic,
                "thumbnail_profile_pic": thumbnail_profile_pic,
                "zip_code": user_profile.zip_code,
                "city": user_profile.city
                },
            }, status=status.HTTP_200_OK,
        )
