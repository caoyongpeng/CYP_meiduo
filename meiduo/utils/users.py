from django.contrib.auth.backends import ModelBackend
from apps.users.models import User
import re
import logging
logger = logging.getLogger('django')


def get_user_by_usernamemobile(username):
    try:
        if re.match(r'1[3-9]\d{9}', username):
            user = User.objects.get(mobile=username)
        else:
            user = User.objects.get(username=username)
    except Exception as e:
        logger.error(e)
        return None
    else:
        return user
class UsernameMobileModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # try:
        #     if re.match(r'1[3-9]\d{9}',username):
        #         user = User.objects.get(mobile=username)
        #     else:
        #         user = User.objects.get(username=username)
        # except Exception as e:
        #     logger.error(e)
        #     return None
        # else:
        #     if user.check_password(password):
        #         return user
        if request is None:
            try:
                if re.match(r'1[3-9]\d{9}', username):
                    user = User.objects.get(mobile=username,is_staff=True)
                else:
                    user = User.objects.get(username=username,is_staff=True)
            except:
                return None
            if user is not None and user.check_password(password):
                return user
        else:
            user = get_user_by_usernamemobile(username)
            if user is not None and user.check_password(password):
                return user



