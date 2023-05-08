from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from .models import *
from ARbook.forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json



# Create your views here.
def index(request):
    if request.method == 'GET':
        formChir = ChirurgieForm()
        formMove = MovesForm()
        formAlr = AlrForm()
        formNeonat = NeonatForm()
        formAge = AgeForm()
        formMater = MaterForm()
        formComplications = ComplicationsForm()

        context = {'formAge':formAge,'formChir':formChir,'formMove':formMove,'formAlr':formAlr,'formNeonat':formNeonat,'formMater':formMater,'formComplications':formComplications}
        return render (request, "ARbook/index.html", context)
    
    elif request.method == 'POST': 
        forms = [ChirurgieForm(request.POST),
                 MovesForm(request.POST),
                 AlrForm(request.POST),
                 NeonatForm(request.POST),
                 AgeForm(request.POST),
                 MaterForm(request.POST),
                 ComplicationsForm(request.POST)
                 ]
            
        user = User.objects.get(username=request.user)
        for form in forms:
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.interne = user
                    obj.save()  


        return HttpResponseRedirect(reverse('index'))
        



def login_view(request):
    if request.method == 'POST':
        
        #Attempt to sign the user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        #Check if authentication successful
        if user is not None:
            login(request, user)
            if user.is_interne:
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        
        else:
            return render(request, 'ARbook/login.html', {
                'message':'Mauvais email et/ou mot de passe'
            })
    else:
        return render(request, 'ARbook/login.html')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@api_view(['GET'])
def interne_view(request, interne):
    interne_id = User.objects.get(username=interne)

    return Response(interne_id.serialize())

def dashboard(request):
    internes = [user.username for user in User.objects.filter(is_interne=True)]
    print(internes)
    chirurgies = [chir[0] for chir in surgery_choices]

    gestes = []
    for list in [age_choices,vvp_choices,va_choices,bloc_choices,lames_choices,complications_choices]:
        for geste in list:
            gestes.append(geste[0])
    gestes.insert(20,'Rachi Neonat')
    gestes.insert(20,'VVP Neonat')

    context = {'internes':internes, 'internes_list':json.dumps(internes), 'gestes':gestes, 'chirurgies':chirurgies}
    return render(request, 'ARbook/dashboard.html', context)