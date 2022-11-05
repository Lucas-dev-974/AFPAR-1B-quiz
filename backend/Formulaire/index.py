from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nom utilisateur', 
        max_length=70, 
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username_input'
            }
        )
    )
    
    password = forms.CharField(
        label='Mot de passe', 
        max_length=100, 
        required=True,
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password_input'
            }
        ), 
    )


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()