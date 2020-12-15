from django.urls import path, include
from .views.problem import ProblemDetails, ProblemList
from .views.course import CourseList, CourseDetail, CourseSubTopic, CourseProblems, LanguagesList, CourseSubmission


urlpatterns = [
    # path('problems/', ProblemList.as_view()),
    # path('problem/<str:problemcode>', ProblemDetails.as_view()),
    path('courses/', CourseList.as_view()),
    path('course/<str:courseid>/', include([
        path('', CourseDetail.as_view()),
        path('languages/', LanguagesList.as_view()),
        path('<str:course_sub_topic>/', include([
            path('', CourseSubTopic.as_view()),
            path('<str:problemcode>/', include([
                path('', CourseProblems.as_view()),
                path('submission/', include([
                    path('', CourseSubmission.as_view()),
                    path('<str:submissionid>/', CourseSubmission.as_view())
                ]))
            ]))
        ]))
    ])),
]
