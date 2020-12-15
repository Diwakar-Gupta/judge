from rest_framework import serializers
from . import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'name', 'description', 'locked', 'is_private')

