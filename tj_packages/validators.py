from rest_framework import serializers


def validate_content_type(request):
    content_type = request.content_type
    if str(content_type) != "application/json":
        raise serializers.ValidationError({
            "result": False,
            "msg": "Invalid content type or missing"
            }, code="validation_error",
        )


def validate_device_id(request):
    device = request.META.get("HTTP_DEVICE", "")
    if str(device) == "":
        raise serializers.ValidationError({
            "result": False,
            "msg": "Device id missing or Invalid"
            }, code="validation_error",
        )


def validate_platform(request):
    platform = request.META.get("HTTP_PLATFORM", "")
    if str(platform) == "":
        raise serializers.ValidationError({
            "result": False,
            "msg": "Platform missing or Invalid"
            }, code="validation_error",
        )


def validate_limit_offset(request):
    params = request.query_params
    limit = params.get('limit', '')
    offset = params.get('offset', 0)
    if str(limit).isdigit() is False or str(offset).isdigit() is False:
        raise serializers.ValidationError({
            "result": False,
            "msg": "limit or offset should be numbers"},
            code="validation_error",
        )


def validate_notification_id(request):
    notification_id = request.data.get("notification_id", "")
    if not notification_id:
        raise serializers.ValidationError(
            {"result": False, "msg": "notification_id missing or Invalid"},
            code="validation_error",
        )
