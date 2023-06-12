
AWS_REGION = "us-east-2"

AWS_S3_REGION_NAME = "us-east-2"

# CELERY Detailse
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "LOCAL": {
        'region': 'us-east-2',
       # "queue_name_prefix": "vidrivals-local-"
    },
    "DEV": {
        'region': 'us-east-2',
        #"queue_name_prefix": "vidrivals-dev-"
    },
    "STG": {
        'region': 'us-east-2',
       # "queue_name_prefix": "vidrivals-stg-"
    },
}

# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = None


AWS_STORAGE_BUCKET_NAME = {
   # "LOCAL": "dev.myvidrivals",
   # "DEV": "dev.myvidrivals",
   # "STG": "stg.vidrivals",
}

AWS_S3_CUSTOM_DOMAIN = {
    "LOCAL": "d1r0dpdlaij12c.cloudfront.net",
    "DEV": "d1r0dpdlaij12c.cloudfront.net",
    "STG": "d2s0ety1uju0zo.cloudfront.net",
}

# AWS S3 CONFIGURATIONS
AWS_PUBLIC_MEDIA_LOCATION = "media/public"
DEFAULT_FILE_STORAGE = "tj_packages.s3_storage.PublicMediaStorage"

AWS_PRIVATE_MEDIA_LOCATION = "media/private"
PRIVATE_FILE_STORAGE = "tj_packages.s3_storage.PrivateMediaStorage"

AWS_PUBLIC_URL = {
    "LOCAL": "https://%s/%s/" % (
        AWS_S3_CUSTOM_DOMAIN['LOCAL'], AWS_PUBLIC_MEDIA_LOCATION),
    "DEV": "https://%s/%s/" % (
        AWS_S3_CUSTOM_DOMAIN['DEV'], AWS_PUBLIC_MEDIA_LOCATION),
    "STG": "https://%s/%s/" % (
        AWS_S3_CUSTOM_DOMAIN['STG'], AWS_PUBLIC_MEDIA_LOCATION),
}

AWS_STATIC_LOCATION = "static"
STATIC_URL = {
    "LOCAL": "/static/",
    "DEV": "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION),
    "STG": "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION),
}

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_EXPIRE = "36000"

# Encryption Decryption Key
#ENCRYPTION_PASSWORD = "e0hNthUefdCBQ1mQ6rT6xLLrPDBQdxUCumjvYUd6S2w="
#ENCRYPTION_SALT = "vidrivalssalt"
# End

# BASE URL Details
BASE_URL = {
    "LOCAL": "http://127.0.0.1:8000/",
   # "DEV": "https://dev-myvidrivals.myvidhire.com/",
   # "STG": "https://stg-myvidrivals.myvidhire.com/",
}

#FIREBASE_API_KEY = "AIzaSyAzdGOtrgD2xa9SPBwMC0UeWfMkWVPEjZc"

