from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # <-- Here
from backend.Formulaire import *
from backend.lector import *
import json


class AuthView(APIView):
    errors = []
    
    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            
            if user is not None:
                token = RefreshToken.for_user(user)
                return JsonResponse({'token': str(token.access_token)})
            else:
                return JsonResponse({"errors": 'Vos identidiants sont incorrectes'}, status = 401)

        else:
            return JsonResponse({"errors": "Les champs renseigner sont invalides !"})

    def delete(self, request):
        return JsonResponse()

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


def getQuestionWithResponseOptions(questionid):
    question_reponse = {}
    
    question = Questions.objects.get(pk=questionid)

    if question is None: return False
    
    question_reponse['id'] = question.pk
    question_reponse['intitule'] = question.intitule_question
    question_reponse['reponses'] = []


    linked_responses = ReponseALaQuestion.objects.filter(idquestion = questionid)

    for link_reponse in linked_responses:
        print(link_reponse.pk)
        reponse = ReponsesPropose.objects.get(pk=link_reponse.pk)

        question_reponse['reponses'].append({
            'id': reponse.pk,
            'intituler': reponse.intitule_reponse
        })
        
    return question_reponse 


class Question(APIView):
    def get(self, request):
        questionid = request.GET.get('questionid')
        if(questionid.isdigit() == False): return JsonResponse({'status': 'L\'id dois être un nombre entier!'})
        question = getQuestionWithResponseOptions(questionid)
        return JsonResponse(question)

    # TODO 
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            # Pour tous les fichiés présent dans la requête on en récuperent les questionnaires //
            for filename, file in request.FILES.items():
                getQuestionnaire(file)
        return JsonResponse({"ok": 'ok'})


class Salarie(APIView):
    def post(self, request):
        if(len(request.FILES) > 0):
            in_file = []
            for filename, file in request.FILES.items():
                in_file.append(getSalaries(file))
                

        return JsonResponse({"status": True})


class QuizzView(APIView):
    # parser_classes = [FileUploadParser]
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