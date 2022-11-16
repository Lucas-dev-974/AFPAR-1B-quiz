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
        secteur_activiter = fields['sector']
    )

    salarie.set_password(fields['password'])
    salarie.save()

    return salarie

def getQuestionnaire(file, file_name=""):
    # Instanciation de Element Tree pour pouvoir lire le fichier si fichier XML
    tree = ET.parse(file)
    XMLroot = tree.getroot()

    session = Sessions.objects.create()
    # Créer une entité quizz qui à pour nom le nom du fichier 
    quizz = saveQuizz({
        "quizz_name": str(file),
        "sessionid": session.pk,
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

def getSalarieInfos(infos):
    _infos = {}
    _infos['sector_type'] = infos[0]
    _infos['sector_name'] = infos[1]
    _infos['matricul'] = infos[5]
    _infos['nom']     = infos[6]
    _infos['prenom'] = infos[7]
    _infos['naissance'] = infos[8]
    _infos['code_postal'] = infos[12]
    return _infos

def getSectorChief(infos):
    _infos = {}
    _infos['sector_type'] = infos[0]
    _infos['sector_name'] = infos[1]
    _infos['matricul']    = infos[2]
    _infos['name']        = infos[3]
    _infos['last_name']   = infos[4]

    chief = Salarie.objects.filter(matricul = _infos['matricul']).first()

    sector = getOrCreateActivitySector(_infos['sector_type'], _infos['sector_name'])

    if chief is None:
        chief = saveSalarie({
            'email': _infos['matricul'] + '@gmail.com',
            'password': _infos['matricul'] + '1234',
            'nom': _infos['name'],
            'prenom': _infos['last_name'],
            'matricul': _infos['matricul'],
            'sector': sector
        })

    if sector.chef_secteur is None:
        sector.chef_secteur = chief
        sector.save()

    return _infos


def getOrCreateActivitySector(sector_type, sector_name):
    print(sector_type, sector_name)
    sector = SecteursActivite.objects.filter(titre_secteur = sector_name).first()

    if sector is None:
        sector = SecteursActivite.objects.create(
            type_secteur = sector_type,
            titre_secteur = sector_name
        )

    return sector


def getSalaries(file):
    _file = file.read().decode('utf-8').splitlines()
    _file.pop(0)

    for user_infos in _file:
        infos = user_infos.split(';')
        salarie_data = getSalarieInfos(infos)
        sector_infos = getOrCreateActivitySector(salarie_data['sector_type'], salarie_data['sector_name'])

        saveSalarie({
            'email': salarie_data['matricul'] + '@gmail.com',
            'password': salarie_data['matricul'] + '1234',
            'nom': salarie_data['nom'],
            'prenom': salarie_data['prenom'],
            'matricul': salarie_data['matricul'],
            'sector': sector_infos
        })  

        getSectorChief(infos)
    


    
    # for row in reader:
    #     print(row)