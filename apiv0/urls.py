from django.urls import path, include
from .views.problem import ProblemDetails, ProblemList
from .views.courses import CourseList, CourseDetail
from .views.course_sub_topics import CourseSubTopic

urlpatterns = [
    path('problems/', ProblemList.as_view()),
    path('problem/<str:problemcode>', ProblemDetails.as_view()),
    path('courses/', CourseList.as_view()),
    path('course/<str:courseid>', include([
        path('', CourseDetail.as_view()),
        path('/<str:course_sub_topic>', include([
            path('', CourseSubTopic.as_view()),
            path('/<str:problemcode>', ProblemDetails.as_view())
        ]))
    ])),
]