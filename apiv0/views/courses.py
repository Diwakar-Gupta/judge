from oj.models.course import Course
from django.shortcuts import HttpResponse
from django.views import View
import json


class CourseList(View):
    def get(self, request, *args, **kwargs):

        # TODO: filter visible and allowed once
        courses = Course.objects.all()
        
        data = [c.detail(forlist = True) for c in courses]

        return HttpResponse(json.dumps(data), content_type="application/json")

class CourseDetail(View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.filter(id=kwargs.get('courseid'))

        data = {}
    
        if course.count() == 1:
            course = course.first()
            data = course.detail()
        else:
            data = {
                'error': 'code not found'
                }
        
        return HttpResponse(json.dumps(data),content_type="application/json")