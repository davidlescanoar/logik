from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from app.models import Problems
from operator import itemgetter
from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from app.serializers import ProblemSerializer
from rest_framework.response import Response


def puntosObtenidos(solvedBy, username):
    JSON = json.loads(solvedBy)

    if username not in JSON:
        return 0

    return JSON[username]


def asignarColor(puntaje):
    if puntaje == 0:
        return "fila-roja"
    if puntaje == 100:
        return "fila-verde"
    return "fila-amarilla"


def cantidadIntentos(solvedBy):
    JSON = json.loads(solvedBy)

    return len(JSON)


def cantidadAC(solvedBy):
    JSON = json.loads(solvedBy)

    Count_AC = 0

    for i in JSON:
        if JSON[i] == 100:
            Count_AC += 1

    return Count_AC


def getProblems():
    problemas = Problems.objects.all()

    listaProblemas = []

    for i in problemas:
        #puntaje = puntosObtenidos(i.solvedBy, request.user.username)
        puntaje = 0
        color = asignarColor(puntaje)

        listaProblemas.append((i.problem_name, i.problem_points, i.problem_link, puntaje, color, cantidadAC(i.solvedBy),
                               cantidadIntentos(i.solvedBy)))

    return sorted(listaProblemas, key=itemgetter(5), reverse=True)

class ProblemsViewSet(viewsets.ModelViewSet):
    #queryset = Problems.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return json.dumps({'puntaje':0})
