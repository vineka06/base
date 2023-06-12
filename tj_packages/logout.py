import datetime
from users import models

from rest_framework import response, status


def logout(request):

    user = request.user
    device = request.META.get("HTTP_DEVICE", "")
    platform = request.META.get("HTTP_PLATFORM", "")
    userLoginDetails = models.UserLoginDetails.objects.filter(
        device_id=device, platform=platform, user=user.id, is_active=True
    ).last()
    if not userLoginDetails:
        return response.Response(
            {"result": False, "msg": "Invalid User Login Details"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    userLoginDetails.logout_time = datetime.datetime.now()
    userLoginDetails.save()
    return response.Response(
        {"result": True, "msg": "Logged out successfully"},
        status=status.HTTP_200_OK,
    )
