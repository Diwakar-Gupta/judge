from oj.models.course import Course_Sub_Topics
from django.shortcuts import HttpResponse
from django.views import View
import json


class CourseSubTopic(View):
    def get(self, request, *args, **kwargs):
        course_sub_topics = Course_Sub_Topics.objects.filter(id=kwargs.get('course_sub_topic'))

        data = {}
    
        if course_sub_topics.count() == 1:
            course = course_sub_topics.first()
            
            data = course.detail()
        else:
            data = {
                'error': 'problem code invalid'
                }
        
        return HttpResponse(json.dumps(data),content_type="application/json")