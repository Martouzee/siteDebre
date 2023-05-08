from django import forms
from django.forms import ModelForm
from .models import *

class ChirurgieForm(ModelForm):
    class Meta:
        model = Surgery
        fields = ('chirurgie',)

class NeonatForm(ModelForm):
    class Meta:
        model = Neonat
        fields = ('lame','rachi','vvp')

class AgeForm(ModelForm):
    class Meta:
        model = Age
        fields = ('age',)

class MovesForm(ModelForm):
    class Meta:
        model = BasicMoves
        fields = ('perfusion','voie_aerienne')

class AlrForm(ModelForm):
    class Meta:
        model = ALR
        fields = ('bloc',)

class ComplicationsForm(ModelForm):
    class Meta:
        model = Complications
        fields = ('complication',)

class MaterForm(ModelForm):
    class Meta:
        model = Mater
        fields = ('mater',)