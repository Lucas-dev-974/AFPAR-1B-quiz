from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers

class UploadFileForm(forms.Form):
    mode = forms.CharField(max_length=50)
    file = forms.FileField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)