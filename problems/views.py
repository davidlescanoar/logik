from django.shortcuts import render
from django.http import HttpResponse
import json
from problems.models import Problems

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

def problems(request):
    problemas=Problems.objects.all()

    listaProblemas=[]

    for i in problemas:
        puntaje=puntosObtenidos(i.solvedBy, request.user.username)
        color=asignarColor(puntaje)

        listaProblemas.append((i.problem_name, i.problem_points, i.problem_link, puntaje, color))



    return render(request, 'problems.html', {'problemas':listaProblemas})