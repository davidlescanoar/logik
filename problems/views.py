from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from problems.models import Problems
from operator import itemgetter

def puntosObtenidos(solvedBy, username):
    JSON=json.loads(solvedBy)

    if username not in JSON:
        return 0

    return JSON[username]

def asignarColor(puntaje):
    if puntaje==0:
        return "fila-roja"
    if puntaje==100:
        return "fila-verde"
    return "fila-amarilla"

def cantidadIntentos(solvedBy):
    JSON=json.loads(solvedBy)

    return len(JSON)

def cantidadAC(solvedBy):
    JSON=json.loads(solvedBy)

    Count_AC=0

    for i in JSON:
        if JSON[i]==100:
            Count_AC+=1

    return Count_AC

def problems(request):
    #Si no está autenticado, no puede entrar
    if not request.user.is_authenticated:
        return redirect('/login')

    problemas=Problems.objects.all()

    listaProblemas=[]

    for i in problemas:
        puntaje=puntosObtenidos(i.solvedBy, request.user.username)
        color=asignarColor(puntaje)

        listaProblemas.append((i.problem_name, i.problem_points, i.problem_link, puntaje, color, cantidadAC(i.solvedBy), cantidadIntentos(i.solvedBy)))

    return render(request, 'problems.html', {'problemas':sorted(listaProblemas, key=itemgetter(5), reverse=True)})