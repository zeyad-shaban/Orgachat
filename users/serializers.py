from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from six import text_type
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email").replace(' ', '').lower()
        email_code = attrs.get("password")
        try:
            email_code = int(email_code)
            try:
                self.user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': "User doesn't exist"}, status.HTTP_404_NOT_FOUND)
            # Do the verification with the email_code here, if error, return a response with an error status code
            if int(email_code) == self.user.email_code and self.user.email_code:
                self.user.email_code = None
                self.user.is_confirmed = True
                self.user.save()

                refresh = self.get_token(self.user)
                return {
                    'refresh': text_type(refresh),
                    'access': text_type(refresh.access_token)
                }

        except:
            self.user = get_object_or_404(User, email=email)

            isValidToken = True
            if isValidToken:
                refresh = self.get_token(self.user)
                return {
                    'refresh': text_type(refresh),
                    'access': text_type(refresh.access_token),
                }

        return Response({'error': 'Validation code is not correct'}, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['about'] = user.about
        token['avatarUri'] = user.avatar.url
        token['categories'] = user.categories
        token['friends'] = serialize('json', user.friends.all())

        return token
