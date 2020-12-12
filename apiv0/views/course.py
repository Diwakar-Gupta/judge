from oj.models.course import Course, Course_Sub_Topics
from oj.models.problem import Problem
from django.shortcuts import HttpResponse, get_object_or_404
from django.views import View
import json


def is_user_with_acces(profile, course):
    return not course.is_private or profile in course.private_contestants

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
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponse('post data', content_type="application/json")

class CourseProblems(View):

    def get(self, request, *args, **kwargs):
        problem = Problem.objects.filter(code=kwargs.get('problemcode'))

        data = {}

        if problem.count() == 1:
            problem = problem.first()
            data = {
                'problem': problem.detail()
            }
        else:
            data = {
                'error': 'problem code invalid'
            }

        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request, *args, **kwargs):
        # handle code submission
        courseid = kwargs.get('courseid')
        problemcode = kwargs.get('problemcode')

        try:
            if not is_user_with_acces(request.user, Course.objects.get(id=courseid)):
                return HttpResponse('not')
        except Exception:
            return HttpResponse('exception')
        
        return HttpResponse('response')