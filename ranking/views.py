from django.shortcuts import render
from django.http import HttpResponse
from problems.models import Problems
import json
from accounts.models import Account
from django.contrib.auth.models import User

# Create your views here.
def ranking(request):
    #Problemas
    _GET=Problems.objects.all()

    #Diccionario par almacenar el puntaje de cada usuario
    data={}

    #Todos los usuarios registrados en el sistema de Logik
    users=User.objects.all()

    #Inicializo el diccionario con 0s
    for user in users:
        data[str(user)]=0

    #Recorro la lista de problemas
    for i in _GET:
        #Paso string a diccionario para saber quienes resolvieron el problema y qué puntaje obtuvieron
        usuarios=json.loads(i.solvedBy)

        #Por cada usuario que haya resuelto el problema
        for _USER,_PUNTAJE in usuarios.items():
            #Sumo al puntaje de ese usuario
            data[_USER]+=_PUNTAJE

    #Ordeno por puntaje, esto es lo que se muestra en pantalla
    ranking=sorted(data.items(), key=lambda item: item[1], reverse=True)

    return render(request, 'ranking.html', {'ranking':ranking})