from django.shortcuts import render
from django.http import HttpResponse
from app.models import *
import json
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
        #Solo agrego a los usuarios que no están en la blacklist
        if not BlackList.objects.filter(black_user=str(user)).exists():
            data[str(user)]=0

    #Recorro la lista de problemas
    for i in _GET:
        #Paso string a diccionario para saber quienes resolvieron el problema y qué puntaje obtuvieron
        usuarios=json.loads(i.solvedBy)

        #Por cada usuario que haya resuelto el problema
        for _USER,_PUNTAJE in usuarios.items():
            #No tengo que agregar a los usuarios de la blacklist
            if BlackList.objects.filter(black_user=str(_USER)).exists():
                continue
            #Sumo al puntaje de ese usuario
            data[_USER]+=_PUNTAJE

    #Ordeno por puntaje, esto es lo que se muestra en pantalla
    ordenar=sorted(data.items(), key=lambda item: item[1], reverse=True)

    #Ranking final
    ranking=[]

    #Enteros que determinan el puesto de los usuarios
    ultimoPuntaje=-1
    puestoActual=1
    puesto=1

    #Armo el vector con los resultados
    for i in ordenar:
        if i[1]!=ultimoPuntaje:
            ultimoPuntaje=i[1]
            puestoActual=puesto

        ranking.append([puestoActual, i[0], i[1]])

        puesto+=1

    return render(request, 'ranking.html', {'ranking':ranking})