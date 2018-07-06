from django.contrib.auth.models import User

class EmailAuthenticationBackend(object):
    '''
    Authentication via e-mail
    '''

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)

            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
