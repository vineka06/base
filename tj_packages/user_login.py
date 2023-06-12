import datetime
from django.contrib import auth

from users import models

User = auth.get_user_model()


def update_user_login_details(
        user: User, device_id: str, platform: str, ip_address: str):
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)
    user.last_login = current_time
    user.save()
    userLoginDetails = models.UserLoginDetails(
        user=user,
        device_id=device_id,
        platform=str(platform).lower(),
        ip_address=ip_address,
        login_time=current_time,
    )
    userLoginDetails.save()
