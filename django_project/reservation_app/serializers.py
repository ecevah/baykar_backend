from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from .models import Customers

class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Özel token alanları ekleyin
        token['name'] = user.name
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = Customers.objects.get(username=username)
            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)

                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)

                # Özelleştirilmiş yanıtlar ekleyin
                data['username'] = user.username
                data['name'] = user.name

                return data
        except Customers.DoesNotExist:
            raise AuthenticationFailed('No active account found with the given credentials')
