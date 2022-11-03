from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.shortcuts import render
from django.http import JsonResponse


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)

def dashHTML(request):
    return render(request, 'dashboard.html')

def loginHTML(request):
    return render(request, 'login.html')


