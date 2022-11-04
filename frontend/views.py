from django.shortcuts import render

def dashHTML(request):
    return render(request, 'dashboard.html')

def loginHTML(request):
    return render(request, 'login.html')
