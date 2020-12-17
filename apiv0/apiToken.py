from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from oj.models import Profile
from django.contrib import auth


@api_view(['POST'])
@permission_classes([AllowAny,])
def googleAuth(request):
    postdata = json.loads(request.body.decode('utf-8'))
    token = postdata['token'] or request.POST.get('token')
    try:
    # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_CLIENT_ID)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
        email = idinfo['email']
        user = User.objects.filter(email = email)
        if user.exists():
            user = user.get()
        else:
            username = email.split("@")[0]
            last_name = idinfo['family_name']
            first_name = idinfo['given_name']
            email_verified = idinfo['email_verified']
            user = User(username = username,
                email = email,
                is_active = email_verified,
                last_name = last_name,
                first_name=first_name
            )
            user.set_unusable_password()
            user.save()
            Profile(user=user).save()
        auth.login(request, user)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
    except ValueError:
    # Invalid token
        pass
    return Response('r u kidding me')


from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import password_validation

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
# @csrf_exempt
def api_change_password(request):
    postcredentials = json.loads(request.body.decode('utf-8'))
    print(postcredentials)
    oldpassword = postcredentials["oldpassword"]
    newpassword = postcredentials['newpassword']
    
    user = request.user

    if  user.has_usable_password() == False or user.check_password(oldpassword):
        user.set_password(newpassword)
        user.save()
        Token.objects.filter(user = user).delete()
        return Response()
    

    return Response('Wrong Credentials',status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def password_reset(request):
    user = request.user
    user.set_unusable_password()
    user.save()
    return Response(status=status.status.HTTP_200_OK)


@api_view(['GET'])
def api_logout(request):
    user = request.user
    user.auth_token.delete()
    return Response()