from django.shortcuts import render
from random import randint
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from twilio.rest import Client
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from phonenumber_field.validators import validate_international_phonenumber
User = get_user_model()


def index(request):
    return render(request, 'users/index.html', {"installs": User.objects.count()})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(('POST',))
def register(request):
    phone_number = request.data.get('phone_number').replace(' ', '')

    # Validate phone number
    try:
        validate_international_phonenumber(phone_number)
    except:
        return Response({'error': f"{phone_number} Is Invalid phone number"}, status.HTTP_400_BAD_REQUEST)

    # Save validation code
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        user = User.objects.create(
            phone_number=phone_number, username=phone_number)
    except Exception as error:
        return Response({'error': f'Internal Server Error 500 \n Please report this problem to us officialorgachat@gmail.com'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    user.phone_code = randint(99999, 999999)
    user.save()

    # Send the validation code
    try:
        account_sid = "AC17578aff15c18d15b452885c627b351f"
        auth_token = "cb454bd3db12a58f07eb35e52edd1491"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Orgachat code {user.phone_code}',
            from_='+13157534823',
            to=str(user.phone_number)
        )
    except:
        return Response({'error': f"Coudn't send validation code to {phone_number}" }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'successfully send validation code'}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def all_users(request):
    q = request.GET.get("q")
    if q:
        users = User.objects.filter(Q(username__icontains=q) | Q(
            email__icontains=q) | Q(country__icontains=q))
    else:
        users = User.objects.filter(
            ~Q(id=request.user.id))

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends(request):
    serializer = UserSerializer(request.user.friends.all(), many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_account(request):
    try:
        request.user.username = request.data.get('username')
        request.user.about = request.data.get('about')
        request.user.save()
        return Response({"message": "successfully udpated"}, status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": "Internal Server Error 500"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
