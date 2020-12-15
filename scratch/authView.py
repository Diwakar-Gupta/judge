from rest_framework import status
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import HttpResponse


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
            user.save()
        auth.login(request, user)
        return Response(idinfo)
    except ValueError:
    # Invalid token
        pass
    return Response('r u kidding me')


@api_view(['GET'])
def whoami(request):
    user = request.user
    res = {
        'username': user.username,
        'is_anonymous': user.is_anonymous
    }
    print(res)
    return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny,])
def api_login(request):

    username = request.data["username"]
    password = request.data["password"]

    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return Response({
        'username': user.username,
        'is_anonymous': user.is_anonymous
    },status=status.HTTP_200_OK)

    return Response({
        'username': '',
        'is_anonymous': True
    },status=status.HTTP_400_BAD_REQUEST)


import json
# @api_view(['POST'])
def api_change_password(request):
    postcredentials = json.loads(request.body.decode('utf-8'))
    print(postcredentials)
    username = postcredentials["username"]
    oldpassword = postcredentials["oldpassword"]
    newpassword = postcredentials['newpassword']

    user = auth.authenticate(request, username=username, password=oldpassword)

    if user == request.user:
        user.set_password(newpassword)
        user.save()
        return HttpResponse()
    return HttpResponse()
    


@api_view(['GET'])
@permission_classes([AllowAny,])
def api_logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)