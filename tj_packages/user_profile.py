from django.contrib import auth
from django.db import models as django_models
from users import models
from tj_packages import image_optimization
from datetime import date
from time import time

User = auth.get_user_model()


def create_user_profile(
        user: User, source: str, mobile_number: str, country_code: str,
        otp_verification_code: int, is_active: bool,
        bio: str, date_of_birth: date, otp_verified=False) -> django_models.QuerySet:
    user_profile = models.UserProfileDetails(
        user=user, source=str(source).lower().strip(),
        mobile_number=mobile_number,
        country_code=country_code,
        otp_verification_code=otp_verification_code,
        otp_verified=otp_verified,
        is_active=is_active,
        bio=bio,
        date_of_birth=date_of_birth
    )
    user_profile.save()
    return user_profile


def update_profile_pic(
        image: object, user: User, profile: models.UserProfileDetails):
    ext = str(image.name).split(".")[-1]
    print(time, type(time))
    image_name = f"profile{user.id}_{int(time())}.{ext}"
    thumb_size = (128, 128)
    medium_size = (356, 356)
    thumb_image = image_optimization.get_optimized_image(
        image, image_name, 80, ext, thumb_size)
    medium_image = image_optimization.get_optimized_image(
        image, image_name, 70, ext, medium_size)
    normal_image = image_optimization.get_optimized_image(
            image, image_name, 70, ext)
    profile.thumbnail_profile_pic = thumb_image
    profile.medium_profile_pic = medium_image
    profile.profile_pic = normal_image
    profile.save()
    return profile