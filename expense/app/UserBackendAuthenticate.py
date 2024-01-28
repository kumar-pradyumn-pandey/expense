from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import *

class CustomBackendAuthenticate(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if '@' in username:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None
            else:
                if user.check_password(password):
                    return user
            return None
