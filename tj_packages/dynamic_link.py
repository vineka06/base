import requests
from rest_framework import serializers
from vid_rivals_project import constants


def generate_dynamic_link(link: str):
    url = f"https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={constants.FIREBASE_API_KEY}"  # noqa
    data = {
            "dynamicLinkInfo": {
                "domainUriPrefix": "https://links.vidrivals.com",
                "link": link,
                "androidInfo": {
                    "androidPackageName": "com.vidrivals",
                    "androidFallbackLink": link,
                    "androidMinPackageVersionCode": "1"
                    },
                "iosInfo": {
                    "iosBundleId": "com.techjays.VidRivals",
                    "iosFallbackLink": link
                    }
            },
            "suffix": {
                "option": "UNGUESSABLE"
            }
        }
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        response_data = response.json()
        short_link = response_data.get("shortLink", "")
        return short_link
    else:
        raise serializers.ValidationError(
            {
                "result": False,
                "msg": "Error in generating dynamic link."
            }, code="validation_error",
        )
