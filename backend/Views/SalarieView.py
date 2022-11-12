from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.Formulaire import *
from backend.lector import *
from backend.models import *

class SalarieView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if(len(request.FILES) > 0):
            in_file = []
            for filename, file in request.FILES.items():
                in_file.append(getSalaries(file))
                

        return JsonResponse({"status": True})