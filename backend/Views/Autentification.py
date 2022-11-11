from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.Formulaire import *
from backend.lector import *
import json
from django.utils.html import escape
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

class TestToken(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse({'success': True})

        
# Inscrit le fichier dans le serveur 
def handle_uploaded_file(f):
    upload_dir = 'backend/questionnaires/'

    t = open( upload_dir + f.name, 'w')
    t.close()

    with open( upload_dir + f.name, 'wb+') as destination:
        print('ok 2')
        for chunk in f.chunks():
            destination.write(chunk)

    

class HelloView(APIView):
    # Permet de vérifier si le demandeur de la requête à bien fourni un token signé
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)

    def post(self, request):
        
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            for filename, file in request.FILES.items():
                getQuestionnaire(file)
        return JsonResponse({"ok": 'ok'})






class SalarieView(APIView):
    def post(self, request):
        if(len(request.FILES) > 0):
            in_file = []
            for filename, file in request.FILES.items():
                in_file.append(getSalaries(file))
                

        return JsonResponse({"status": True})


class QuizzView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        quizzid = request.GET.get('quizzid')    
        if(quizzid.isdigit() == False): return JsonResponse({'status': 'L\'id dois être un nombre entier!'})

        quizz_data = {}

        quizz = Quizz.objects.get(pk=quizzid)
        possede_questions = Possede.objects.filter(idquizz = quizz.pk)
        
        quizz_data['quizzid']   = quizz.pk
        quizz_data['questions'] = []

        for posseder in possede_questions:
            question_id = posseder.idquestion_id
            quizz_data['questions'].append( getQuestionWithResponseOptions(question_id))

        return JsonResponse(quizz_data)

    
    def post(self, request):
        quizz = request.data
        print(request.user.email)
        for reponse in quizz['reponses']:
            histo_reponse_quizz = HistoriqueReponsesSelectionner.objects.create(
                matricule_salarie_id = request.user.id,
                idquizz_id = quizz['quizzid'],
                idreponse_id = reponse['reponseid'],
                idquestion_id = reponse['questionid']
            )

            print(reponse)
        return JsonResponse(quizz, safe=False)


def createSession(request):
    print(type(request.POST))
    print('ko')

    return JsonResponse({'status': 'ok'})

