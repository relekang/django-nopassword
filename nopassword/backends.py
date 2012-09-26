from django.contrib.auth.models import User
from nopassword.models import LoginCode

class EmailBackend:
    
    def authenticate(self, username, password=None)
        try:
            user = User.objects.get(username=username)
            return LoginCode.check(user, password)
        except (TypeError, User.DoesNotExist)
            return False
