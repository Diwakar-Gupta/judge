from rest_framework import serializers
from oj.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'description',
        )
        model = Course