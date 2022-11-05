""" extract transform load v0 
M. convertit tout un dossier de fichiers XML en 1 seul TXT résultat
O. crée un fichier texte avec tous les qcm (trame générale)
I. exploite une série de fichiers XML, structure à decouvrir
"""
import xml.etree.ElementTree as ET
from os import walk 


# https://courspython.com/classes-et-objets.html
# https://www.journaldunet.fr/web-tech/developpement/1499365-comment-creer-un-nouveau-fichier-text-txt-en-python/
# https://bobbyhadz.com/blog/python-unicodeencodeerror-charmap-codec-cant-encode-characters-in-position
class Texte:
    def __init__(self,txt=''):
        self.text = txt 
    def add(self, txtAdd):
        self.text += txtAdd + '\n'
    def createLog(self, ficLog) : 
        file = open(ficLog, "w", encoding='iso-8859-1')
        file.write(self.text) 
        file.close()
    def console(self) :
        print('\n\n'+self.text)

# https://www.journaldunet.fr/web-tech/developpement/1202869-comment-lister-tous-les-fichiers-d-un-repertoire-en-python/
def  getListeFichiers(dossier) :
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in walk(dossier):
        listeFichiers.extend(fichiers)
        break                             # donc niv1 seulement
    # print(listeFichiers)
    return listeFichiers


def traiterUnFichier( fichierXml ) : 
    
    mytree = ET.parse( fichierXml )
    myroot = mytree.getroot()
        
    # debut de fichier
    noq=0 
    ret = Texte()

    # boucle de traitement des X elements du fichier
    for question in myroot:
        # debut de question
        noq+= 1
        ret.add( 'Question ' + str(noq) + ' ---------------------------------------')
        ret.add( question.find('intitule').text )

        bonne = question.attrib.get('bonne')
        compteur = 1

        # boucle de traitement 
        for reponse in question.find('listerep'):
            if compteur == int(bonne):
                ret.add(' [ * ] ' + reponse.text )
            else:
                ret.add(' [ ] ' + reponse.text ) 

            compteur += 1
        
        # fin de question
        ret.add('feedback : ' + question.find('feedback').text )
        ret.add('')
    
    # fin du fichier
    return ret.text


monRepertoire = './questionnaires/'
listeFichiers = getListeFichiers(monRepertoire)

""" boucle pour traiter chaque fichier trouvé
"""
out = Texte()
out.add ('RESULTATS\n' ) 

#for fich in listeFichiers[0:3] :    # pour test!
for fich in listeFichiers :
    out.add ( '#########################################################################')
    out.add ( '###  QUESTIONNAIRE : ' + fich )
    out.add ( '#########################################################################')
    print(fich)    # verbose
    out.add ( traiterUnFichier( monRepertoire + fich ) )

out.createLog('./questionnaires_v0.txt') 
#out.console()

print( str(len(listeFichiers)) + ' fichiers traités' )