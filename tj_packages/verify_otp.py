from rest_framework import serializers, response, status
from django.core import exceptions
from django.conf import settings
from django.contrib import auth
from tj_packages import user_token, user_login, send_new_user_signup, encrypt_decrypt
from vid_rivals_app import models as vidrivals_models
from users import models
from vid_rivals_app import controllers

User = auth.get_user_model()


def verify_otp(request: object):

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
    mobile_number = data.get("mobile_number", "")
    country_code = data.get("country_code", "")
    otp_verification_code = data.get("otp_verification_code", 0)

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
                    mobile_number=mobile_number, country_code=country_code)
        )
    except exceptions.ObjectDoesNotExist:
        raise serializers.ValidationError({
                "result": False,
                "msg": "Invalid OTP or User"
            }, code="validation_error",
        )

    if user_profile_details.otp_verified:
        return response.Response({
            "result": True,
            "msg": "OTP Already Verified"
            }, status=status.HTTP_200_OK,
        )
    else:
        existing_verfication_code = user_profile_details.otp_verification_code
        if int(existing_verfication_code) == int(otp_verification_code):
            user_profile_details.otp_verified = True
            user_profile_details.is_active = True
            user_profile_details.user.is_active = True
            user_profile_details.save()
            user_profile_details.user.save()
            user_login.update_user_login_details(
                user=user_profile_details.user, device_id=device_id,
                platform=platform, ip_address=ip_address)
            token = user_token.get_token(
                user=user_profile_details.user)
            configuration_master = vidrivals_models.ConfigurationMaster.objects.all().first()
            controllers.MoneyBagController().add_schnikes(
                schnikes=configuration_master.new_user_schnike_amount,
                user=user_profile_details.user)
            transaction_type = (
                controllers.MoneyBagTransactionTypeController().get(
                    name='Signup Schnikes')
            )
            controllers.MoneyBagTransactionController().add_transaction(
                schnikes=configuration_master.new_user_schnike_amount,
                user=user_profile_details.user,
                duel_id=None, transaction_type=transaction_type.id)
            staff_user = User.objects.filter(is_staff=True)
            for user in staff_user:
                data = str(user.username) + "^^^" + str(user.email)
                token_mail = encrypt_decrypt.encrypt(data)
                verification_url = (
                    "%sapi/v1/users/confirm-verification/?verifytoken=%s"
                    % (settings.BASE_URL, token_mail)
                )
                email_data = {
                    "user_id":user_profile_details.user.id, "nickname": user_profile_details.user.username, "first_name": user_profile_details.user.first_name, "last_name": user_profile_details.user.last_name, "mobile_number": user_profile_details.mobile_number, "email": user_profile_details.user.email} # noqa
                send_new_user_signup.send_new_user_signup(
                    user.username, user.email, verification_url, email_data)
            invited_duel_ids = vidrivals_models.InvitedUser.objects.filter(
                mobile_number=mobile_number).values_list("duel_id", flat=True)
            duel = vidrivals_models.Duel.objects.filter(
                id__in=invited_duel_ids)
            duel.update(invited_user=user_profile_details.user)
            vidrivals_models.InvitedUser.objects.filter(
                mobile_number=mobile_number).delete() # noqa
            return response.Response({
                "result": True,
                "msg": "OTP Verified Successfully",
                "data": {
                    "user_id": user_profile_details.user.pk,
                    "token": token.key,
                    "mobile_number": mobile_number,
                    "country_code": user_profile_details.country_code,
                    "fist_name": user_profile_details.user.first_name,
                    "last_name": user_profile_details.user.last_name,
                    "email": user_profile_details.user.email,
                    "zip_code": user_profile_details.zip_code,
                    "city": user_profile_details.city,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response({
                "result": False,
                "msg": "Invalid OTP"
                }, status=status.HTTP_400_BAD_REQUEST,
            )
