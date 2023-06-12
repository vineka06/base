from django.contrib import auth
from rest_framework.authtoken.models import Token

User = auth.get_user_model()


def get_token(user: User):
    token = Token.objects.get_or_create(user=user)[0]
    return token
