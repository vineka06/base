from packaging import version
from rest_framework import serializers as rest_serializers

# APP platforms
android = "android"
ios = "ios"

APP_LINK = {
    "android": "https://play.google.com/store/apps/details?id=com.vidrivals",
    "ios": "https://apps.apple.com/in/app/vid-rivals/id1592321777",
}

# App Update Content
APP_VERSIONS = {
    "android": ["1.0.4","1.0.5","1.0.6","1.0.7","1.0.8","1.0.9","1.10","1.11","1.12","1.13","1.14","1.15", "1.16"], # noqa
    "ios": ["1.0.2","1.0.3","1.0.4","1.0.5","1.0.6","1.0.7","1.0.8","1.0.9","1.10","1.11","1.12","1.13","1.14","1.15", "1.16"], # noqa
}

LATEST_APP_VERSION = {
    "android": "1.16",
    "ios": "1.16",
}

FORCE_UPDATE_MIN_VERSION = {
    "android": "1.15",
    "ios": "1.15",
}

UPDATE_TYPE = {
    "force_update": 1,
    "light_update": 2,
    "no_update": 3,
}

FORCE_UPDATE_CONTENT = {
    "android": {
        "type": UPDATE_TYPE["force_update"],
        "title": "App update v1.15",
        "desc": "What's New",
        "points": [
            "General Improvements & Bug fixes",
        ],
        "link": APP_LINK[android],
    },
    "ios": {
        "type": UPDATE_TYPE["force_update"],
        "title": "App update v1.15",
        "desc": "What's New",
        "points": [
            "General Improvements & Bug fixes"
        ],
        "link": APP_LINK[ios],
    },
}

LIGHT_UPDATE_CONTENT = {
    "android": {
        "type": UPDATE_TYPE["light_update"],
        "title": "App update v1.15",
        "desc": "What's New",
        "points": [
            "General Improvements & Bug fixes",
        ],
        "link": APP_LINK[android],
    },
    "ios": {
        "type": UPDATE_TYPE["light_update"],
        "title": "App update v1.15",
        "desc": "What's New",
        "points": [
            "General Improvements & Bug fixes",
        ],
        "link": APP_LINK[ios],
    },
}

NO_UPDATE_CONTENT = {
    "type": UPDATE_TYPE["no_update"],
}
# End


def get_app_update_content(app_version: str, device: str):
    try:
        app_verison = version.parse(app_version)
    except ValueError:
        raise rest_serializers.ValidationError({
                "result": False,
                "msg": "app_version should be float",
            }, code="validation_error"
        )

    if not device:
        raise rest_serializers.ValidationError({
            "result": False,
            "msg": "device is missing or empty"
            }, code="validation_error"
        )
    device = str(device).lower()
    if not str(device) == "ios" and not str(device) == "android":
        raise rest_serializers.ValidationError({
            "result": False,
            "msg": "Invalid or wrong device"
            }, code="validation_error"
        )

    if str(app_verison) not in APP_VERSIONS[device]:
        raise rest_serializers.ValidationError({
                "result": False,
                "msg": "Invalid app_version",
            }, code="validation_error"
        )
    # return NO_UPDATE_CONTENT
    if app_verison == version.parse(LATEST_APP_VERSION[device]):
        return NO_UPDATE_CONTENT

    if app_verison <= version.parse(FORCE_UPDATE_MIN_VERSION[device]):
        return NO_UPDATE_CONTENT
    else:
        return NO_UPDATE_CONTENT