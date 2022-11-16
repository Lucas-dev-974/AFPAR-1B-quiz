from django.contrib import admin
from django.urls import path, include
from backend.Views import *
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('login', AuthView.as_view()),
    path('token/check', TokenVerifyView.as_view()),

    path('quizz/imports', QuizzImport.as_view()), # POST
    path('quizz/creer',   QuizzImport.as_view()), # POST
    path('quizz',         QuizzView.as_view()),   # GET
    path('quizzs',         QuizzView.as_view()),

    path('question', Question.as_view()),
    
    path('salaries/import', SalarieView.as_view()),
    path('salaries', SalarieView.as_view()),

    # POST répondre à un quizz
    # GET récuperer un quizz via son id
    # PATCH modifier un quizz
]
