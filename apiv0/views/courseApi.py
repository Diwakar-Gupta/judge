## TODO when rest api will get implemented

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from oj.models import Course

class ListCourse(APIView):

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return Response(courses)