from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Recommended as Recomendados
import json
from django.contrib.auth.models import User


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


# Create your views here.
def recommended(request):
    # Si no está autenticado, no puede entrar
    if not request.user.is_authenticated:
        return redirect('/login')

    # Si se llenó el formulario
    if request.method == 'POST':
        # Obtengo los datos del formulario
        _ProblemName = request.POST['problem_name']
        _ProblemLink = request.POST['problem_link']
        _OnlineJudge = request.POST['Online-Judge']

        # Si el problema no existía
        if not Recomendados.objects.filter(problem_link=_ProblemLink).exists():
            # Inserto el problema en la DB
            Recomendados.objects.create(problem_name=_ProblemName, problem_link=_ProblemLink, judge=_OnlineJudge,
                                        solvedBy="{}")

        # Recargo la página
        return redirect('/recommended')

    # Caso general: se quiere ver la tabla de problemas
    problemas = Recomendados.objects.all()

    # Lista de problemas
    listaProblemas = []

    # Por cada problema
    for i in problemas:
        # Me fijo el puntaje que obtuvo
        puntaje = puntosObtenidos(i.solvedBy, request.user.username)
        # Le asigno un color en base al puntaje
        color = asignarColor(puntaje)

        # Un problema vale 100 puntos
        _PROBLEM_POINTS = 100

        # Agrego el problema a la lista que se va a mostrar
        listaProblemas.append((i.problem_name, _PROBLEM_POINTS, i.problem_link, puntaje, color))

    # Diccionario par almacenar el puntaje de cada usuario
    data = {}

    # Todos los usuarios registrados en el sistema de Logik
    users = User.objects.all()

    # Inicializo el diccionario con 0s
    for user in users:
        data[str(user)] = 0

    # Recorro la lista de problemas
    for i in problemas:
        # Paso string a diccionario para saber quienes resolvieron el problema y qué puntaje obtuvieron
        usuarios = json.loads(i.solvedBy)

        # Por cada usuario que haya resuelto el problema
        for _USER, _PUNTAJE in usuarios.items():
            # Sumo al puntaje de ese usuario
            data[_USER] += _PUNTAJE

    # Ordeno por puntaje, esto es lo que se muestra en pantalla
    ordenar = sorted(data.items(), key=lambda item: item[1], reverse=True)

    # Ranking final
    ranking = []

    # Enteros que determinan el puesto de los usuarios
    ultimoPuntaje = -1
    puestoActual = 1
    puesto = 1

    # Armo el vector con los resultados
    for i in ordenar:
        if i[1] != ultimoPuntaje:
            ultimoPuntaje = i[1]
            puestoActual = puesto

        ranking.append([puestoActual, i[0], i[1]])

        puesto += 1

    return render(request, 'recommended.html', {'problemas': listaProblemas, 'ranking': ranking})