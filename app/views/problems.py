from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from app.models import Problems
from operator import itemgetter


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


def problems_by_year(year, username):
    problemas = Problems.objects.filter(year=year)

    listaProblemas = []

    for i in problemas:
        puntaje = puntosObtenidos(i.solvedBy, username)
        color = asignarColor(puntaje)

        listaProblemas.append((i.problem_name, i.problem_points, i.problem_link, puntaje, color, cantidadAC(i.solvedBy),
                               cantidadIntentos(i.solvedBy)))

    return sorted(listaProblemas, key=itemgetter(5), reverse=True)


def problems(request):
    # Si no está autenticado, no puede entrar
    if not request.user.is_authenticated:
        return redirect('/login')

    problems = {
        '2020': problems_by_year(2020, request.user.username),
        '2021': problems_by_year(2021, request.user.username),
    }

    return render(request, 'problems.html', {'problemas': problems})
