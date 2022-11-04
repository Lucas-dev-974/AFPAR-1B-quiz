from django.contrib import admin
from django.urls import path, include
from backend.Views import *

urlpatterns = [
    path('login', AuthView.as_view()),
    path('helloworld', HelloView.as_view())
]