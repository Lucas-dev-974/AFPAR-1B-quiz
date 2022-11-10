""" extract transform load v0 
M. convertit tout un dossier de fichiers XML en 1 seul TXT résultat
O. crée un fichier texte avec tous les qcm (trame générale)
I. exploite une série de fichiers XML, structure à decouvrir
"""
import xml.etree.ElementTree as ET
from .models import *

def saveQuizz(fields):
    quizz = Quizz.objects.create(
        nom_quizz = fields['quizz_name'],
        idsession_id = fields['sessionid'],
        id_sa_id = fields['secteurid']
    )

    return quizz

def linkQuestionToQuizz(fields): 
    linked_quizz_session = Possede.objects.create(
        idquizz_id    = fields['quizzid'],
        idquestion_id = fields['questionid']
    )


def saveQuestion(fields):
    question = Questions.objects.create(
        intitule_question=fields['intituler']
    )
    return question

def saveResponseOption(fields):
    reponse =  ReponsesPropose.objects.create(
        intitule_reponse=fields['intituler'],
        bonne_reponse=fields['bonne']
    )

    return reponse

def linkResponseToQuestion(responseid, questionid):
    link_response_question = ReponseALaQuestion.objects.create(idquestion_id = questionid, idreponse_id = responseid)
    return link_response_question


def saveSalarie(fields):
    salarie = Salarie.objects.create(
        email = fields['email'],
        nom   = fields['nom'],
        prenom = fields['prenom'],
        matricul = fields['matricul'],
    )

    salarie.set_password(fields['password'])
    salarie.save()

def getQuestionnaire(file, file_name=""):
    # Instanciation de Element Tree pour pouvoir lire le fichier si fichier XML
    tree = ET.parse(file)
    XMLroot = tree.getroot()

    # Créer une entité quizz qui à pour nom le nom du fichier 
    quizz = saveQuizz({
        "quizz_name": str(file),
        "sessionid": 1,
        "secteurid": 1
    })

    
    # Récupère toutes les question présent dans le fichier
    questions = XMLroot.findall('question')

    #Pour toute les question du fichier 
    for question in questions:

        # On récupère les informations du questionnaire
        bonne = question.attrib.get('bonne')
        titre = question.findtext('titre')
        intituler = question.findtext('intitule')
        
        # On créer ici une entité question 
        question_ = saveQuestion({
            'titre': titre,
            'intituler': intituler
        })

        # Puis on créer une entité qui est le lien entre la question et le quizz (entité possede)
        linked_question_to_quizz = linkQuestionToQuizz({
            "quizzid": quizz.pk,
            "questionid": question_.pk
        })

        # On vas ensuite récupérer les réponse possible 
        reponses = question.find('listerep').findall('reponse')
        
        for (idx, reponse) in enumerate(reponses):
            bonne_ = None
            if(idx + 1 == int(bonne)):
                bonne_ = True
            else:
                bonne_ = False

            reponse_ = saveResponseOption({
                'intituler': reponse.text,
                'bonne': bonne_
            })

            linkResponseToQuestion(questionid=question_.pk, responseid=reponse_.pk)

def getSalaries(file):
    _file = file.read().decode('utf-8').splitlines()
    print(_file[1].split(';'))


    for user_infos in _file:
        infos = user_infos.split(';')
        secteur = infos[0]
        secteur_name = infos[1]
        matricule_salarie = infos[5]
        salarie_name = infos[6]
        salarie_last_name = infos[7] 
        salarie_naissance = infos[8]
        salarie_code_postal = infos[12]

        saveSalarie({
            'email': matricule_salarie + '@gmail.com',
            'nom': salarie_name,
            'prenom': salarie_last_name,
            'matricul': matricule_salarie,
            'password': matricule_salarie + '1234'
        })

    
    # for row in reader:
    #     print(row)