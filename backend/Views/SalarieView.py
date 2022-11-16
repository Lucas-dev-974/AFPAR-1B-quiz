from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.Formulaire import *
from backend.lector import *
from backend.models import *
from .utilsForView import *
from rest_framework import serializers

class SalarieView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)

        salaries = Salarie.objects.all().values()
          
        return JsonResponse(list(salaries), safe=False)

    def post(self, request):
        if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)
        
        if(len(request.FILES) > 0):
            in_file = []
            for filename, file in request.FILES.items():
                in_file.append(getSalaries(file))
                

        return JsonResponse({"status": 'Salairés, Secteur, Chef de secteur importer avec succès'})