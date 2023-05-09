from django.contrib.auth.models import AbstractUser
from django.db import models

internes = 14

surgery_choices = [
    ('Rachis','Rachis'),
    ('Orthopedie','Orthopedie'),
    ('Viscerale','Viscerale'),
    ('Urologie','Urologie'),
    ('Thoracique','Thoracique'),
    ('Urgences','Urgences'),
    ('Neonatologie','Neonatologie'),
    ('ORL','ORL'),
    ('Ophtalmologie','Ophtalmologie'),
    ('Stomatologie','Stomatologie'),
    ('Gastro','Gastro'),
    ('Imagerie','Imagerie')
]

age_choices = [
    ('< 1 mois','< 1 mois'),
    ('< 1 an','< 1 an'),
    ('< 3 ans','< 3ans'),
    ('< 10 ans','< 10 ans')
]

va_choices = [
    ('Masque Facial','Masque Facial'),
    ('Masque Laryngé','Masque Laryngé'),
    ('Intubation','Intubation')
]

vvp_choices = [
    ('Main','Main'),
    ('Saphène','Saphène')
]

bloc_choices = [
    ('Rachianesthesie','Rachianesthesie'),
    ('Péridurale','Péridurale'),
    ('Caudale','Caudale'),
    ('Bloc maxillaire','Bloc maxillaire'),
    ('Pudendal Neurostim','Pudendal Neurostim'),
    ('Pudendal Echo','Pudendal Echo'),
    ('Ilioinguinal','Ilioinguinal'),
    ('Penien','Penien')
]

lames_choices = [
    ('Oxford','Oxford'),
    ('Miller','Miller'),
    ('Macintosh','Macintosh')
]

complications_choices = [
    ('Spasme','Spasme'),
    ('Choc','Choc'),
    ('Saignement','Saignement'),
    ('ACR','ACR')
]

mater_choices = [
    ('Echorepérage','Echorepérage'),
    ('Péri-Rachi combinée','Péri-Rachi combinée'),
    ('Déambulatoire','Déambulatoire'),
    ('Rachianesthésie','Rachianesthésie')
]

# Create your models here.
class User(AbstractUser):
    is_interne = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def serialize(self):
        # create dictionaries for each surgery, move, and bloc choice
        surgeries = {surgery[0]: {'total': Surgery.objects.filter(chirurgie=surgery[0]).count(),
                            'perso': Surgery.objects.filter(chirurgie=surgery[0], interne=self).count()}
                    for surgery in surgery_choices}
            
        voie_veineuse = {vvp[0]: {'total': BasicMoves.objects.filter(perfusion=vvp[0]).count(),
                    'perso': BasicMoves.objects.filter(perfusion=vvp[0], interne=self).count()}
                for vvp in vvp_choices}
        
        voie_aerienne = {va[0]: {'total': BasicMoves.objects.filter(voie_aerienne=va[0]).count(),
                                 'perso': BasicMoves.objects.filter(voie_aerienne=va[0], interne=self).count()}
                                 for va in va_choices}
        
        age = {a[0]: {'total': Age.objects.filter(age=a[0]).count(),
                      'perso': Age.objects.filter(age=a[0], interne=self).count()}
                      for a in age_choices}
        
        complication = {comp[0]: {'total': Complications.objects.filter(complication=comp[0]).count(),
                                  'perso': Complications.objects.filter(complication=comp[0], interne=self).count()}
                                  for comp in complications_choices}
        
        lame_neonat = {lame[0]: {'total': Neonat.objects.filter(lame=lame[0]).count(),
                                 'perso': Neonat.objects.filter(lame=lame[0], interne=self).count()}
                                 for lame in lames_choices}
        
        rachi_neonat = {'Rachi Neonat': {'total': Neonat.objects.filter(rachi=True).count(),
                                         'perso': Neonat.objects.filter(rachi=True, interne=self).count()}}
        
        vvp_neonat = {'VVP Neonat': {'total': Neonat.objects.filter(vvp=True).count(),
                                     'perso': Neonat.objects.filter(vvp=True, interne=self).count()}}

        alr = {bloc[0]: {'total': ALR.objects.filter(bloc=bloc[0]).count(),
                    'perso': ALR.objects.filter(bloc=bloc[0], interne=self).count()}
            for bloc in bloc_choices}
        
        # calculate the mean for each surgery, move, bloc, etc choice
        for item in [surgeries, voie_veineuse, voie_aerienne, alr, age, complication, lame_neonat, rachi_neonat, vvp_neonat]:
            for choice in item:
                item[choice]['moyenne'] = round(item[choice]['total'] / internes,2)
                item[choice]['difference'] = item[choice]['moyenne']-item[choice]['perso'] 
        
        # return the serialized data
        return {
            'Interne': self.username,
            'Age':age,
            'Chirurgies': surgeries,
            'Voie veineuse': voie_veineuse,
            'Voie aérienne': voie_aerienne,
            'Complication': complication,
            'Lame Neonat': lame_neonat,
            'VVP Neonat': vvp_neonat,
            'Rachi Neonat': rachi_neonat,
            'ALR': alr,
        }


class Surgery(models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_suregery')
    chirurgie = models.CharField(max_length=25,choices=surgery_choices,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Age(models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_age')
    age = models.CharField(max_length=25,choices=age_choices,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class BasicMoves (models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_moves')
    perfusion = models.CharField(max_length=25,choices=vvp_choices, blank=True)
    voie_aerienne = models.CharField(max_length=25,choices=va_choices, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class ALR (models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_alr')
    bloc = models.CharField(max_length=25,choices=bloc_choices,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Neonat (models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_neonat')
    lame = models.CharField(max_length=25,choices=lames_choices,blank=True)
    rachi = models.BooleanField(default=False,blank=True)
    vvp = models.BooleanField(default=False,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Complications (models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_complication')
    timestamp = models.DateTimeField(auto_now_add=True)
    complication = models.CharField(max_length=25,choices=complications_choices,blank=True)


class Mater (models.Model):

    interne = models.ForeignKey('User', on_delete=models.CASCADE, related_name='interne_mater')
    timestamp = models.DateTimeField(auto_now_add=True)
    mater = models.CharField(max_length=25,choices=mater_choices,blank=True)

