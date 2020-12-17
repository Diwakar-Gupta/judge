from django.http.response import Http404
from requests.adapters import Response
from oj.models.submission import Submission, SubmissionCached, SubmissionSource
from oj.models.runtime import Language
from oj.models.course import Course, Course_Sub_Topics, Course_Submissions, Course_Profile
from oj.models.problem import Problem
from oj.models.runtime import Language
from oj.models.profile import Profile
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from rest_framework.views import APIView

FORBIDDEN_MESSAGE = 'U Dont have Permission to see this'

def is_user_with_acces(profile, course):
    return not course.is_private or (profile != None and profile.courses.filter(id=course.id).exists())

def languages_allowed(course):
    languages = Language.objects.all()
    return languages

def get_course_object(self):
    slug_value = self.kwargs.get('courseid')
    return get_object_or_404(Course, id = slug_value)

def get_sub_topic_object(self):
    slug_value = self.kwargs.get('course_sub_topic')
    return get_object_or_404(Course_Sub_Topics, id = slug_value)

def get_sourse_submission_object(self):
    slug_value = self.kwargs.get('submissionid')
    return get_object_or_404(Course_Submissions, id = slug_value)

class CourseObjectMixin(object):
    model = Course
    slug_field = 'id'
    slug_url_kwarg = 'courseid'

    def get_object(self):
        slug_value = self.kwargs.get('courseid')
        return get_object_or_404(Course, id = slug_value)


class LanguagesList(View):

    def get(self, *args, **kwargs):
        languages = languages_allowed(get_object_or_404(Course, id=kwargs.get('courseid')))
        return HttpResponse(json.dumps([l.detail(forlist=True) for l in languages]), content_type="application/json")


class CourseList(APIView):
    def get(self, request, *args, **kwargs):
        print(request.user)
        # from django.contrib import auth
        # auth.login(request, auth.models.User.objects.all()[0])

        user = request.user
        profile = request.user.profile if not user.is_anonymous else None

        public_courses = Course.objects.filter(is_private=False)
        private_course = []
        if profile:
            private_course = profile.courses.filter(is_private=True)
        
        data = [c.detail(forlist = True) for c in public_courses]
        data += [c.detail(forlist = True) for c in private_course]

        # raise Http404
        return HttpResponse(json.dumps(data), content_type="application/json")


class CourseDetail(CourseObjectMixin, APIView):
    slug_field = 'id'
    slug_url_kwarg = 'courseid'

    def get(self, request, *args, **kwargs):

        user = request.user
        profile = user.profile if not user.is_anonymous else None

        course = self.get_object()
        if course.is_private:
            if not profile or not profile.courses.filter(id=course.id).exists():
                return HttpResponseForbidden(FORBIDDEN_MESSAGE)
            
        data = course.detail()
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    def post(self, request, *args, **kwargs):
        postdata = json.loads(request.body.decode('utf-8'))



class CourseSubTopicMixin(object):
    model = Course_Sub_Topics
    slug_field = 'id'
    slug_url_kwarg = 'course_sub_topic'

    def get_object(self):
        slug_value = self.kwargs.get('course_sub_topic')
        return get_object_or_404(Course_Sub_Topics, id = slug_value)


class CourseSubTopic(CourseSubTopicMixin, APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        course = get_course_object(self)

        if user.is_anonymous and course.is_private:
            raise Http404()

        profile = user.profile if not user.is_anonymous else None

        if not is_user_with_acces(profile, course):
            raise Http404()

        course_sub_topics = self.get_object()
        data = course_sub_topics.detail()        
        return HttpResponse(json.dumps(data),content_type="application/json")
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return HttpResponse('post data', content_type="application/json")


class CourseProblemMixin(CourseObjectMixin, CourseSubTopicMixin, object):
    model = Problem
    slug_field = 'code'
    slug_url_kwarg = 'problemcode'

    def get_object(self):
        slug_value = self.kwargs.get('problemcode')
        return get_object_or_404(Problem, code = slug_value)
    
    def get_course_object(self):
        return super(CourseObjectMixin, self).get_object()
    
    def get_subtopic_object(self):
        return super(CourseSubTopicMixin, self).get_object()
    


class CourseProblems(CourseProblemMixin, LanguagesList, APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        
        profile = user.profile if not user.is_anonymous else None

        problem = self.get_object()
        course = get_course_object(self)

        if course.is_private and not is_user_with_acces(profile, course):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
        
        data = {}

        languages = languages_allowed(course)
        data = {
            'problem': problem.detail(),
        }
        data['allowed_languages']= [l.detail(forlist=True) for l in languages]
        return JsonResponse(data)


# class CourseSubmissionList()


class CourseSubmissionMixin(object):
    model = Course_Submissions
    slug_field = 'id'
    slug_url_kwarg = 'submissionid'

    def get_object(self):
        slug_value = self.kwargs.get('submissionid')
        return get_object_or_404(Course_Submissions, id = slug_value)
    
    def get_course_object(self):
        slug_value = self.kwargs.get('courseid')
        return get_object_or_404(Course, id = slug_value)
    
    def get_problem_object(self):
        slug_value = self.kwargs.get('problemcode')
        return get_object_or_404(Problem, code = slug_value)

class CourseSubmission(CourseSubmissionMixin, APIView):

    def get(self, request, *args, **kwargs):
        user = request.user

        course_submission = self.get_object()
        
        submission = course_submission.submission
        serilized = submission.serilize()

        return JsonResponse(serilized)


    def post(self, request, *args, **kwargs):
        # new submision
        user = request.user
        if user.is_anonymous:
            return HttpResponseForbidden('U need to SignIn to submit code')

        profile = user.profile if not user.is_anonymous else None
        
        course = get_course_object(self)

        if course.is_private and not is_user_with_acces(profile, course):
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
        
        postdata = json.loads(request.body.decode('utf-8'))
        print(postdata)
        try:
            language = get_object_or_404(Language, key=postdata['key'])
        except Exception:
            return HttpResponse(json.dumps({'error':'cant find this language'}))
        source = postdata.get('code')
        problem = self.get_problem_object()
        # user = request.user.profile
        user = request.user
        if user.is_anonymous:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE)
        
        # course = self.get_course_object()
        # profile = user.profile
        
        submission = Submission(user=profile, language=language, problem=problem)
        submission.save()
        SubmissionSource(submission=submission, source=source).save()
        
        try:
            pass
            # submission.judge()
        except ConnectionRefusedError:
            pass

        course_profile, created = Course_Profile.objects.get_or_create(
            user=profile,
            course = course
        )
        if created:
            course.total_participantes += 1
            course.save()
            course_profile.save()
        
        course_submission = Course_Submissions(course = course, submission=submission, profile=course_profile)
        course_submission.save()
        cached_submission = SubmissionCached(submission=submission)
        cached_submission.save()
        return JsonResponse(cached_submission.key, safe=False)
        # return JsonResponse(2, safe=False)
        

def cached_Submission(request, token):
    return JsonResponse(get_object_or_404(SubmissionCached, key=token).get_serilized())


from rest_framework import generics
from ..serializers import coursesubmission as serilizer

class ListCourseSubmission(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = serilizer.Course_Submissions

    def dispatch(self, request, *args, **kwargs):
        self.queryset = Course.objects.filter(is_private = False)
        return super().dispatch(request, *args, **kwargs)