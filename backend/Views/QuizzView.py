from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from backend.Formulaire import *
from backend.models import *
from backend.lector import *
from .utilsForView import *

# Méthode qui permet de récuperer des une question via son ID et les ses réponses possible 
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

def getQuizz(quizz_id):
    quizz = {}

    _quizz = Quizz.objects.get(pk=quizz_id)
    if _quizz is None: return False

    quizz['id']  = _quizz.pk
    quizz['nom'] = _quizz.nom_quizz

    linked_question = Possede.objects.filter(idquizz = _quizz.pk)

    quizz['questions'] = []

    for qlink in linked_question:
        quizz['questions'].append(getQuestionWithResponseOptions(qlink.idquestion.pk))
    return quizz


class Question(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        questionid = request.GET.get('questionid')
        if(questionid.isdigit() == False): return JsonResponse({'status': 'L\'id dois être un nombre entier!'})
        question = getQuestionWithResponseOptions(questionid)
        return JsonResponse(question)

    def post(self, request):
        if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            # Pour tous les fichiés présent dans la requête on en récuperent les questionnaires //
            for filename, file in request.FILES.items():
                getQuestionnaire(file)
        return JsonResponse({"ok": 'ok'})


class QuizzView(APIView):
    # Si le client n'a pas fourni de Token de connexion alor une erreur 401 unauthorized lui est retourner
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if(request.GET.get('quizzid') is None): return JsonResponse({'status': 'Le paramètre quizzid dois être renseigner dans l\'uri de la requête !'})
        quizzid = request.GET.get('quizzid')    
        if(quizzid.isdigit() == False): return JsonResponse({'status': 'L\'id dois être un nombre entier!'}, 400)

        quizz_data = {}

        quizz = Quizz.objects.get(pk=quizzid)
        possede_questions = Possede.objects.filter(idquizz = quizz.pk)
        
        quizz_data['quizzid']   = quizz.pk
        quizz_data['nom']       = quizz.nom_quizz
        quizz_data['questions'] = []

        for posseder in possede_questions:
            question_id = posseder.idquestion_id
            quizz_data['questions'].append( getQuestionWithResponseOptions(question_id))

        return JsonResponse(quizz_data)

    
    def post(self, request):
        quizz = request.data
        
        for reponse in quizz['reponses']:
            histo_reponse_quizz = HistoriqueReponsesSelectionner.objects.create(
                matricule_salarie_id = request.user.id,
                idquizz_id = quizz['quizzid'],
                idreponse_id = reponse['reponseid'],
                idquestion_id = reponse['questionid']
            )
            print(histo_reponse_quizz)
        return JsonResponse(quizz, safe=False)
    

class QuizzImport(APIView):
    # Permet de vérifier si le demandeur de la requête à bien fourni un token signé
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)
    
        if('imports' in request.path): 
            form = UploadFileForm(request.POST, request.FILES)

            if form.is_valid():
                for filename, file in request.FILES.items():
                    getQuestionnaire(file)
            return JsonResponse({"ok": 'ok'})
        
        if('creer' in request.path):
            print(request.data)
            session = Sessions.objects.create(date_de_deploiment = request.data['session_deploiment'])
            quizz   = Quizz.objects.create(nom_quizz = request.data['quizz_name'], idsession_id = session.pk, id_sa_id = 1)

            for question in request.data['quizz_questions']:
                question_ = Questions.objects.create(intitule_question = question['intitule'])
                linkQuestionToQuizz({
                    "quizzid": quizz.pk,
                    'questionid': question_.pk
                })

                for reponse in question['responses_options']:
                    reponse = ReponsesPropose.objects.create(intitule_reponse = reponse['intitule'], bonne_reponse = reponse['bonne'])
                    linkResponseToQuestion(reponse.pk, question_.pk)
                

                # question = Questions.objects.create
            
            return JsonResponse(getQuizz(quizz_id=quizz.pk))
