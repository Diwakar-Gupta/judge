from django.urls import path
from .views import problem

urlpatterns = [
    path('problems/', problem.ProblemList.as_view()),
    path('problem/<str:code>', problem.ProblemDetails.as_view())
]