from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

class AuthView(APIView):
    errors = []

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            token = RefreshToken.for_user(user)
            return JsonResponse({'token': str(token.access_token)})
        else:
           return JsonResponse({"errors": 'Désoler vos identidiants sont incorrectes'}, status = 401)

    def delete(self, request):
        return JsonResponse()