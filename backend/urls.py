from django.contrib import admin
from django.urls import path, include
from backend.Views import *

urlpatterns = [
    path('login', AuthView.as_view()),
    path('token/check', TestToken.as_view()),

    path('question/imports', HelloView.as_view()),
    path('question', Question.as_view()),
    path('question', Question.as_view()), 
    
    path('salaries/import', SalarieView.as_view()),
    
    path('quizz', QuizzView.as_view())
]
