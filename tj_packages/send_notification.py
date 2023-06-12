from django.db import models as django_models
from pyfcm import FCMNotification
from vid_rivals_project import settings


class FCMNotificationModel:

    def send_notification(
            self, notification_datas: django_models.QuerySet,
            message_title: str, message_body: str, data_message: dict,
            sound="Default", badge=0):
        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        android_fcm_tokens = []
        ios_fcm_tokens = []

        for obj in notification_datas:
            if str(obj.platform) == "android":
                android_fcm_tokens.append(obj.notification_id)
            else:
                ios_fcm_tokens.append(obj.notification_id)

        android_data_message = data_message
        android_data_message["title"] = message_title
        android_data_message["body"] = message_body
        android_data_message["badge"] = badge
        if android_fcm_tokens:
            push_service.notify_multiple_devices(
                registration_ids=android_fcm_tokens,
                data_message=android_data_message,
                badge=badge)
        if ios_fcm_tokens:
            push_service.notify_multiple_devices(
                registration_ids=ios_fcm_tokens,
                message_title=message_title,
                message_body=message_body,
                data_message=data_message, sound=sound,
                badge=badge)

    def send_notification_test(
        self, platform: str, notification_id: str,
            message_title: str, message_body: str):
        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        android_fcm_tokens = []
        ios_fcm_tokens = []

        if str(platform) == "android":
            android_fcm_tokens.append(notification_id)
        else:
            ios_fcm_tokens.append(notification_id)

        message_title = message_title
        message_body = message_body
        data_message = {"hello": "sdfdfs"}
        android_data_message = data_message
        android_data_message["title"] = message_title
        android_data_message["body"] = message_body

        if android_fcm_tokens:
            push_service.notify_multiple_devices(
                registration_ids=android_fcm_tokens,
                data_message=android_data_message)
        if ios_fcm_tokens:
            push_service.notify_multiple_devices(
                registration_ids=ios_fcm_tokens,
                message_title=message_title,
                message_body=message_body,
                data_message=data_message, sound="Default")
