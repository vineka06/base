from datetime import date, datetime
from django.contrib.auth.models import User
from django.core import validators, exceptions
from django.db import models as django_models
from rest_framework import serializers
from users import models
from tj_packages import user_profile


def create_user(
        request: object, otp_verification_code: int, is_active=False
        ) -> django_models.QuerySet:
    data = request.data
    first_name = data.get("first_name", "").title().strip()
    last_name = data.get("last_name", "").title().strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    country_code = data.get("country_code", "")
    mobile_number = data.get("mobile_number", "")
    # zip_code = data.get("zip_code", "")
    # city = data.get("city", "")
    password = data.get("password", "")
    source = data.get("source", "")
    date_of_birth = data.get("date_of_birth", "")
    if not first_name:
        raise serializers.ValidationError(
            {"result": False, "msg": "First Name is required"},
            code="validation_error",
        )

    if not last_name:
        raise serializers.ValidationError(
            {"result": False, "msg": "Last Name is required"},
            code="validation_error",
        )
    if first_name and len(first_name) > 25:
        raise serializers.ValidationError(
            {"result": False, "msg": "First name length should not exceed more than 25 characters"},
            code="validation_error",
        )
    if last_name and len(last_name) > 25:
        raise serializers.ValidationError(
            {"result": False, "msg": "Last name length should not exceed more than 25 characters"},
            code="validation_error",
        )
    if not username:
        raise serializers.ValidationError(
            {"result": False, "msg": "Nickname is required"},
            code="validation_error",
        )
    if username and len(username) > 20:
        raise serializers.ValidationError(
            {"result": False, "msg": "Nickname must have min of 4 and max of 20 characters"},
            code="validation_error",
        )
    if username and len(username) < 4:
        raise serializers.ValidationError(
            {"result": False, "msg": "Nickname must have min of 4 and max of 20 characters"},
            code="validation_error",
        )
    if not date_of_birth:
        raise serializers.ValidationError(
            {"result": False, "msg": "Date of birth is required"},
            code="validation_error",
        )
    else:
        date_of_birth_format = datetime.strptime(date_of_birth, "%Y-%m-%d")
    if not email:
        raise serializers.ValidationError(
            {"result": False, "msg": "Enter a valid email address"},
            code="validation_error",
        )

    if username:
        if models.UserProfileDetails.objects.filter(
                user__username=username, otp_verified=False).exists():
            User.objects.filter(username=username).delete()

        if models.UserProfileDetails.objects.filter(
                user__username=username).exclude(
                    mobile_number=mobile_number, country_code=country_code
                    ).exists():
            raise serializers.ValidationError(
                {"result": False, "msg": "Nickname already taken. Please choose a different one"},
                code="validation_error",
            )

    if not mobile_number:
        raise serializers.ValidationError(
            {"result": False, "msg": "Mobile number missing or empty."},
            code="validation_error",
        )

    if not country_code:
        raise serializers.ValidationError(
            {"result": False, "msg": "Country code missing or empty."},
            code="validation_error",
        )

    # if not zip_code:
    #     raise serializers.ValidationError(
    #         {"result": False, "msg": "Zip code is required"},
    #         code="validation_error",
    #     )

    # if not city:
    #     raise serializers.ValidationError(
    #         {"result": False, "msg": "City is required"},
    #         code="validation_error",
    #     )

    if not password:
        raise serializers.ValidationError(
            {"result": False, "msg": "Password is required"},
            code="validation_error",
        )

    if not source:
        raise serializers.ValidationError(
            {"result": False, "msg": "Source missing or empty."},
            code="validation_error",
        )

    if mobile_number:
        if models.UserProfileDetails.objects.filter(
                mobile_number=mobile_number, is_active=True).exists():
            raise serializers.ValidationError(
                {"result": False, "msg": "Account already exists. Please Sign in"},
                code="validation_error",
            )

    # if not date_of_birth:
    #     raise serializers.ValidationError(
    #         {"result": False, "msg": "Date of birth is required"},
    #         code="validation_error",
    #     )
    # else:
    #     date_of_birth_format = datetime.strptime(date_of_birth, "%Y-%m-%d")
    today = date.today()
    if today.year - date_of_birth_format.year - ((today.month, today.day) < (date_of_birth_format.month, date_of_birth_format.day)) < 18: # noqa
        raise serializers.ValidationError(
            {"result": False, "msg": "You must be 18 years old to use Vid Rivals"},
            code="validation_error",
        )
    if email:
        try:
            validators.validate_email(email)
        except exceptions.ValidationError:
            raise serializers.ValidationError(
                {"result": False, "msg": "Enter a valid Email ID"},
                code="validation_error",
            )

        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError(
                {"result": False, "msg": "Email address must be unique."},
                code="validation_error",
            )

    if (
        country_code and mobile_number and
        models.UserProfileDetails.objects.filter(
            mobile_number=mobile_number, otp_verified=True,
            user__is_active=True).exists()):
        raise serializers.ValidationError({
            "result": False,
            "msg": "Account already exists. Please Sign in"},
            code="validation_error",
        )

    user_profile_data = models.UserProfileDetails.objects.filter(
        mobile_number=mobile_number, otp_verified=False,
        user__is_active=False).first()
    if user_profile_data:
        user_profile_details = update_user_and_profile_details(
            user_profile_details=user_profile_data, first_name=first_name,
            last_name=last_name, email=email,
            password=password, source=source, mobile_number=mobile_number,
            country_code=country_code, username=username,
            otp_verification_code=otp_verification_code, is_active=is_active,
            date_of_birth=date_of_birth)
        user = user_profile_details.user
    else:
        user = User(
            first_name=str(first_name).strip(),
            last_name=str(last_name).strip(),
            email=str(email).strip(),
            username=str(username),
            is_active=is_active,
        )
        user.set_password(password)
        user.save()
        bio = "I am a Vid Rivals user"
        user_profile_details = user_profile.create_user_profile(
            user=user, source=source, mobile_number=mobile_number,
            country_code=country_code,
            otp_verification_code=otp_verification_code, is_active=is_active,
            bio=bio, date_of_birth=date_of_birth, otp_verified=False
            )

    return user, user_profile_details


def update_user_and_profile_details(
        user_profile_details: django_models.QuerySet, first_name: str,
        last_name: str, email: str, password: str,
        source: str, mobile_number: str, country_code: str, username: str,
        otp_verification_code: str, date_of_birth: date, is_active: bool) -> django_models.QuerySet:
    user_profile_details.user.first_name = str(first_name).strip()
    user_profile_details.user.last_name = str(last_name).strip()
    # user_profile_details.zip_code = str(zip_code).strip()
    # user_profile_details.city = str(city).strip()
    user_profile_details.user.username = str(username).strip()
    user_profile_details.user.email = str(email).strip()
    user_profile_details.user.is_active = is_active
    user_profile_details.user.set_password(password)
    user_profile_details.user.save()
    user_profile_details.source = str(source).lower().strip()
    user_profile_details.mobile_number = mobile_number
    user_profile_details.country_code = country_code
    user_profile_details.otp_verification_code = otp_verification_code
    user_profile_details.date_of_birth = date_of_birth
    user_profile_details.save()
    return user_profile_details


def update_profile_details(
        user_profile_details: django_models.QuerySet, username: str,
        first_name: str, last_name: str, zip_code: str, city: str, email: str, source: str,
        bio: str, street_address: str, date_of_birth: date) -> django_models.QuerySet:
    user_profile_details.user.username = str(username)
    user_profile_details.user.first_name = str(first_name).strip()
    user_profile_details.user.last_name = str(last_name).strip()
    user_profile_details.user.email = str(email).strip()
    user_profile_details.user.save()
    user_profile_details.zip_code = str(zip_code).strip() if zip_code else None
    user_profile_details.city = str(city).strip() if city else None
    user_profile_details.source = str(source).lower().strip()
    user_profile_details.bio = str(bio).strip()
    user_profile_details.street_address = str(street_address).strip() if street_address else None # noqa
    user_profile_details.date_of_birth = date_of_birth
    user_profile_details.save()
    return user_profile_details