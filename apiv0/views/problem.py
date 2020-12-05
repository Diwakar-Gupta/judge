from oj.models.problem import Problem
from django.shortcuts import HttpResponse
from django.views import View
import json

# ProblemList
# ProblelmDetail

class ProblemList(View):
    def get(self, request, *args, **kwargs):
        problems = Problem.objects.all()
        data = []

        for p in problems:
            if p.contestcount == 0:
                data.append({
                    'code': p.code,
                    'name': p.name
                })

        return HttpResponse(json.dumps({'problems': data}), content_type="application/json")


class ProblemDetails(View):

    def get(self, request, *args, **kwargs):
        problem = Problem.objects.filter(code=kwargs.get('code'))

        data = {}
    
        if problem.count() == 1:
            problem = problem.first()
            data = {
                'problem': {
                    'code':problem.code,
                    'name': problem.name,
                    'description': problem.description
                }
            }
        else:
            data = {
                'error': 'problem code invalid'
                }
        
        return HttpResponse(json.dumps(data),content_type="application/json")
