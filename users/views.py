from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import render
from random import randint
from django.db.models.query_utils import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


def index(request):
    return render(request, 'users/index.html', {"installs": User.objects.count()})

def privacypolicy(request):
    return render(request, 'users/privacypolicy.html')

def termsandconditions(request):
    return render(request, 'users/termsandconditions.html')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(('POST',))
def register(request):
    email = request.data.get('email').replace(' ', '').lower()

    # Save validation code
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create(email=email, username=''.join(
            [i for i in email.split('@')[0] if not i.isdigit()]))
    except Exception as error:
        return Response({'error': f'Internal Server Error 500 \n Please report this problem to us officialorgachat@gmail.com'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    user.email_code = randint(99999, 999999)
    user.save()

    # Send the validation code
    try:
        send_mail('Orgachat Validation Code',
                  f'Your validation code is {user.email_code}.', 'officialorgachat@gmail.com', (user.email,), fail_silently=False)
    except:
        return Response({'error': f"Coudn't send validation code to {email}. \n Tip: we support Gmails only for now"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'successfully send validation code'}, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def all_users(request):
    request.user.update_last_seen()
    q = request.GET.get("q")
    if q:
        users = User.objects.filter(Q(username__icontains=q) | Q(
            email__icontains=q), is_confirmed=True)
    else:
        users = User.objects.filter(~Q(id=request.user.id), is_confirmed=True)

    return Response([user.to_json() for user in users])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends(request):
    request.user.update_last_seen()
    serializer = UserSerializer(request.user.friends.all(), many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_account(request):
    request.user.update_last_seen()
    try:
        if request.FILES.get('file'):
            request.user.avatar = request.FILES.get('file')
            request.user.username = request.GET.get('username')
            request.user.about = request.GET.get('about')
        else:
            request.user.username = request.data.get('username')
            request.user.about = request.data.get('about')
        request.user.save()
        return Response({"message": "successfully udpated"}, status.HTTP_200_OK)
    except:
        return Response({"error": "Internal Server Error 500"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_expo_push_token(request):
    try:
        request.user.expo_push_token = request.data.get('expoPushToken')
        request.user.save()
        return Response({'user': request.user.to_json()}, status.HTTP_200_OK)
    except:
        return Response({'error': f"Internal Server Error 500"}, status.HTTP_500_INTERNAL_SERVER_ERROR)