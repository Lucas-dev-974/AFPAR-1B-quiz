from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.Formulaire import *
from backend.lector import *
from backend.models import *

class AuthView(APIView):
    
    def post(self, request):
        
        login_form = LoginSerializer(data=request.data)
        
        if login_form.is_valid():
            username = request.data['username']
            password = request.data['password']

            # Vérifie si les identifiant de l'utilisateur sont corrects
            authenticated_user = authenticate(email = username, password = password)

            if authenticated_user is not None:

                # Si oui alors on le connect
                # Une fois cette fonction appeler les informations de l'utilisateur se retrouve dans le var request -> request.user
                login(request, authenticated_user)

                # puis on instancie un object user qui contient les infos de l'utilisateur 
                _user = {
                    "id": request.user.id,
                    'matricul': request.user.matricul,
                    'nom': request.user.nom,
                    'prenom': request.user.prenom,
                    'email': request.user.email,
                    'role': request.user.role,
                    'code_postal': request.user.code_postal,
                    'naissance': request.user.naissance,
                    'ville': request.user.ville,
                    'secteur': {
                        'type_secteur': request.user.secteur_activiter.type_secteur,
                        'titre_secteur': request.user.secteur_activiter.titre_secteur
                    }
                }

                # ensuite on génère un token de connexion qui seras utiliser dans toutes les requêtes au niveau du front end 
                token = RefreshToken.for_user(authenticated_user)
                return JsonResponse({'token': str(token.access_token), 'user': _user})
            else:
                return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)

        else:
            return JsonResponse({"errors": "Les champs renseigner sont invalides !"}, status=400    )

    def delete(self, request):
        return JsonResponse()


def createSession(request):
    print(type(request.POST))
    print('ko')

    return JsonResponse({'status': 'ok'})

