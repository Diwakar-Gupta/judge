from oj.models import Course_Submissions
from rest_framework import serializers


class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'submission.result',
        )
        model = Course_Submissions