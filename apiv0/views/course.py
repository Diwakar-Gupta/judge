from oj.models.submission import Submission, SubmissionSource
from oj.models.runtime import Language
from oj.models.course import Course, Course_Sub_Topics, Course_Submissions, Course_Profile
from oj.models.problem import Problem
from oj.models.runtime import Language
from oj.models.profile import Profile
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
import json


def is_user_with_acces(profile, course):
    return not course.is_private or profile in course.private_contestants

def languages_allowed(course):
    languages = Language.objects.all()
    return languages


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


class CourseList(View):
    def get(self, request, *args, **kwargs):

        # TODO: filter visible and allowed once
        courses = Course.objects.all()
        
        data = [c.detail(forlist = True) for c in courses]

        return HttpResponse(json.dumps(data), content_type="application/json")


class CourseDetail(CourseObjectMixin, View):
    slug_field = 'id'
    slug_url_kwarg = 'courseid'

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        data = course.detail()
        return HttpResponse(json.dumps(data),content_type="application/json")


class CourseSubTopicMixin(object):
    model = Course_Sub_Topics
    slug_field = 'id'
    slug_url_kwarg = 'course_sub_topic'

    def get_object(self):
        slug_value = self.kwargs.get('course_sub_topic')
        return get_object_or_404(Course_Sub_Topics, id = slug_value)


class CourseSubTopic(CourseSubTopicMixin, View):

    def get(self, request, *args, **kwargs):
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
    


class CourseProblems(CourseProblemMixin, LanguagesList, View):

    def get(self, request, *args, **kwargs):
        problem = self.get_object()
        course = self.get_course_object()

        data = {}

        languages = languages_allowed(course)
        data = {
            'problem': problem.detail(),
        }
        data['problem']['allowed_languages']= [l.detail(forlist=True) for l in languages]

        return HttpResponse(json.dumps(data), content_type="application/json")


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

class CourseSubmission(CourseSubmissionMixin, View):

    def get(self, request, *args, **kwargs):
        course_submission = self.get_object()
        
        if course_submission.profile.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden()
        
        submission = course_submission.submission
        serilized = submission.serilize()

        return HttpResponse(json.dumps(serilized))

    def post(self, request, *args, **kwargs):
        # new submision
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
            return HttpResponseForbidden()
        
        course = self.get_course_object()
        profile = user.profile
        
        submission = Submission(user=profile, language=language, problem=problem)
        submission.save()
        SubmissionSource(submission=submission, source=source).save()
        submission.judge()

        course_profile, created = Course_Profile.objects.get_or_create(
            user=profile,
            course = course
        )
        course_profile.save()
        course_submission = Course_Submissions(course = course, submission=submission, profile=course_profile)
        course_submission.save()
        return HttpResponse(json.dumps(course_submission.id))
        
        