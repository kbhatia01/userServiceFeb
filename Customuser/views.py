import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from Customuser.CustomTokenView import CustomTokenSerializer
from Customuser.service import sign_up_service, login_service
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        print(email)
        user = sign_up_service(email, password, username)

        if user is None:
            return HttpResponse(json.dumps({'error': 'invalid data'}), content_type='application/json')

        token = RefreshToken.for_user(user)
        tokenVal = str(token.access_token)

        return HttpResponse(json.dumps({'token': tokenVal}), content_type='application/json')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        token, err = login_service(email, password)
        if err:
            return HttpResponse(json.dumps({'error': str(err)}), content_type='application/json')

        return HttpResponse(
            json.dumps({'token': token}),
            content_type='application/json')


# TODO: create a method where you take a token in headers and
#  print username of that token's user...


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sayHello(request):

    print(request.user.email)
    return HttpResponse(request.user.email, status=200)
