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
        reponse = ReponsesPropose.objects.get(pk=link_reponse.pk)

        question_reponse['reponses'].append({
            'id': reponse.pk,
            'intituler': reponse.intitule_reponse
        })
        
    return question_reponse 

def quizzForUser(userid):
    user_participation = Participe.objects.filter(userid_id = userid)
    quizzs = []

    for participation in user_participation:
        _quizzs = Quizz.objects.filter(
            idsession = participation.idsession
        )   
        
        for quizz in _quizzs:
            _quizz = {}
            _quizz['id'] = quizz.pk
            _quizz['nom'] = quizz.nom_quizz

            _quizz['questions'] = []
            possede_questions = Possede.objects.filter(idquizz = quizz.pk)

            for posseder in possede_questions:
                question_id = posseder.idquestion_id
                _quizz['questions'].append(getQuestionWithResponseOptions(question_id))
            quizzs.append(_quizz)

        return quizzs


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
        return JsonResponse({"status": 'quizz importer avec succès'})

def getParticipantsForSession(session_id):
    participants = Participe.objects.filter(idsession = session_id)
    print(participants)

class QuizzView(APIView):
    # Si le client n'a pas fourni de Token de connexion alor une erreur 401 unauthorized lui est retourner
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if('quizzs' in request.path):
            if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)
            _quizzs = []
            quizzs = Quizz.objects.all()


            for quizz in quizzs:
                _quizz = {}
                _quizz['nom'] = quizz.nom_quizz
                _quizz['id']  = quizz.pk
                _quizz['in_session'] = {
                    'session_id': quizz.idsession.id,
                    'date_de_deploiement': quizz.idsession.date_de_deploiment
                }

                _quizz['participants'] = Participe.objects.filter(idsession = quizz.idsession.id).count()


                possede_questions = Possede.objects.filter(idquizz = quizz.pk)

                questions = []

                for posseder in possede_questions:
                    question_id = posseder.idquestion_id
                    questions.append(getQuestionWithResponseOptions(question_id))
                
                _quizz['questions'] = questions
                _quizzs.append(_quizz)
            
            return JsonResponse(_quizzs, safe=False)

        else: 
            return JsonResponse(quizzForUser(request.user.id), safe=False)
    
    def post(self, request):
        quizz = request.data
        # return JsonResponse({"status": 1})
        for reponse in quizz['reponses']:
            histo_reponse_quizz = HistoriqueReponsesSelectionner.objects.create(
                matricule_salarie_id = request.user.id,
                idquizz_id    = quizz['quizzid'],
                idreponse_id  = reponse['reponseid'],
                idquestion_id = reponse['questionid']
            )
            
        return JsonResponse(quizz, safe=False)
    

class QuizzImport(APIView):
    # Permet de vérifier si le demandeur de la requête à bien fourni un token signé
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if isAdmin(request) == False: return JsonResponse({'status': 'Vous devez être DSI ou DRH pour importer de nouveaux salariés'}, status = 401)
    
        if('imports' in request.path): 
            form = UploadFileForm(request.POST, request.FILES)
            print(request.FILES)
            
            if form.is_valid():
                for filename, file in request.FILES.items():
                    getQuestionnaire(file)


            return JsonResponse({"ok": 'ok'})
        
        if('creer' in request.path):
            
            session = Sessions.objects.create(date_de_deploiment = request.data['session_deploiment'])
            quizz   = Quizz.objects.create(nom_quizz = request.data['quizz_name'], idsession_id = session.pk, id_sa_id = 1)

            participants= request.data['participants']

            for participant in participants:
                part = Participe.objects.create(userid_id = participant, idsession_id = session.id)

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
