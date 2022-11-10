from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import *



class SecteursActivite(models.Model):
    type_secteur = models.CharField(db_column='Type_secteur', max_length=50)  # Field name made lowercase.
    titre_secteur = models.CharField(max_length=50)



# On instancie ici un model salarié qui serat les utilisateurs de l'app
class Salarie(AbstractUser):
    username    = None
    email       = models.EmailField('email', unique=True)
    nom         = models.CharField(max_length=70)
    prenom      = models.CharField(max_length=70)
    role        = models.CharField('role', default='salarié', max_length=50)
    naissance   = models.DateField(null=True, blank=True)
    code_postal = models.CharField(max_length=30, default="974")
    ville       = models.CharField(max_length=60, blank=True, null=True)
    matricul    = models.CharField(max_length=50, unique=True)
    secteur_activiter = models.ForeignKey(SecteursActivite, on_delete=models.DO_NOTHING, db_column='ID_SA', default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = SalarieManager()

    def __str__(self):
        return self.email


class Sessions(models.Model):
    date_de_deploiment = models.DateField(blank=True, null=True)  # Field name made lowercase.


class Participe(models.Model):
    matricule_salarie = models.ForeignKey(Salarie, models.DO_NOTHING, unique=False)  # Field name made lowercase.
    idsession = models.ForeignKey(Sessions, models.DO_NOTHING, unique=False)  # Field name made lowercase.

class Quizz(models.Model):
    noteminimal = models.IntegerField(db_column='NoteMinimal', blank=True, null=True)  # Field name made lowercase.
    etat_brouillon = models.IntegerField(db_column='Etat_brouillon', blank=True, null=True)  # Field name made lowercase.
    nom_quizz = models.CharField(max_length=70, blank=True, null=True)
    idsession = models.ForeignKey(Sessions, models.DO_NOTHING)  # Field name made lowercase.
    id_sa = models.ForeignKey(SecteursActivite, models.DO_NOTHING, unique=False)  # Field name made lowercase.



class Questions(models.Model):
    feedback_question = models.CharField(max_length=150, blank=True, null=True)  # Field name made lowercase.
    intitule_question = models.CharField(max_length=150, blank=True, null=True)  # Field name made lowercase.
    coeff_bonne_reponse = models.IntegerField(blank=True, null=True)  # Field name made lowercase.


class ReponsesPropose(models.Model):
    bonne_reponse = models.BooleanField(default=False)
    intitule_reponse = models.CharField(max_length=150, null=False, blank=False)



class Possede(models.Model):
    idquizz = models.ForeignKey(Quizz, models.DO_NOTHING, unique=False)  # Field name made lowercase.
    idquestion = models.ForeignKey(Questions, models.DO_NOTHING, unique=False)  # Field name made lowercase.


class ReponseALaQuestion(models.Model):
    idreponse = models.ForeignKey(ReponsesPropose, models.DO_NOTHING, unique=False)  # Field name made lowercase.
    idquestion = models.ForeignKey(Questions, models.DO_NOTHING, unique=False)  # Field name made lowercase.


class HistoriqueReponsesSelectionner(models.Model):
    matricule_salarie = models.ForeignKey(Salarie, models.DO_NOTHING)  # Field name made lowercase.
    idquizz = models.ForeignKey(Quizz, models.DO_NOTHING)  # Field name made lowercase.
    idreponse = models.ForeignKey(ReponsesPropose, models.DO_NOTHING)  # Field name made lowercase.
    idquestion = models.ForeignKey(Questions, models.DO_NOTHING)  # Field name made lowercase.
    date_repondu = models.DateTimeField(blank=True, null=True)
    entrainement = models.BooleanField(blank=True, null=True)  # Field name made lowercase.
