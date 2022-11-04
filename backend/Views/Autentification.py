from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # <-- Here


class AuthView(APIView):
    errors = []
    
    def post(self, request):
        # // TODO utiliser un formulaire pour vérifié les données
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 
        user = authenticate(username=username, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            return JsonResponse({'token': str(token.access_token)})
        else:
           return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)

    def delete(self, request):
        return JsonResponse()


class HelloView(APIView):
    # Permet de vérifier si le demandeur de la requête à bien fourni un token signé
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)