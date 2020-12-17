from rest_framework import generics

from oj.models import Course
from . import serializers


class ListCourse(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def dispatch(self, request, *args, **kwargs):
        self.queryset = Course.objects.filter(is_private = False)
        return super().dispatch(request, *args, **kwargs)


class DetailCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    # authentication_classes = (TokenAuthentication, )

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)