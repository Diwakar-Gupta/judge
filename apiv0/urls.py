from django.urls import path, include
from .views.problem import ProblemDetails, ProblemList
from .views.course import CourseList, CourseDetail, CourseSubTopic, CourseProblems, LanguagesList, CourseSubmission, cached_Submission, ListCourseSubmission

from . import view
from rest_framework.authtoken.views import obtain_auth_token
from . import apiToken

urlpatterns = [
    # path('problems/', ProblemList.as_view()),
    # path('problem/<str:problemcode>', ProblemDetails.as_view()),
    # path('courses/', CourseList.as_view()),
    path('courses/', view.ListCourse.as_view()),
    path('course/<int:pk>/', view.DetailCourse.as_view()),
    # path('hello/', view.HelloView.as_view()),
    path('auth2/', include([
        path('api-token-auth/', obtain_auth_token),
        path('social-google/', apiToken.googleAuth),
        path('logout/', apiToken.api_logout),
        path('change-password/', apiToken.api_change_password),
        path('password-reset/', apiToken.password_reset),
    ])),
    # path('rest-auth/', include('rest_auth.urls')),
    path('cachedsubmission/<str:token>', cached_Submission),
    path('course/<str:courseid>/', include([
        path('', CourseDetail.as_view()),
        path('languages/', LanguagesList.as_view()),
        # path('participants/', ),
        path('<str:course_sub_topic>/', include([
            path('', CourseSubTopic.as_view()),
            path('<str:problemcode>/', include([
                path('', CourseProblems.as_view()),
                path('submission/', include([
                    path('', ListCourseSubmission.as_view()),
                    path('<str:submissionid>/', CourseSubmission.as_view())
                ]))
            ]))
        ]))
    ])),
]
