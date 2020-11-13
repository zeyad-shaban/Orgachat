from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from six import text_type
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        phone_code = int(attrs.get("password"))
        try:
            self.user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': "User doesn't exist"}, status.HTTP_404_NOT_FOUND)
        # Do the verification with the phone_code here, if error, return a response with an error status code
        if int(phone_code) == self.user.phone_code and self.user.phone_code:
            self.user.phone_code = None
            self.user.save()

            refresh = self.get_token(self.user)
            data = {
                'refresh': text_type(refresh),
                'access': text_type(refresh.access_token)
            }
            return data
        return Response({'error': 'Validation code is not correct'}, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token
