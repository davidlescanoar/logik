from django.shortcuts import render
from django.http import HttpResponse
import json
from problems.models import Problems

def problems(request):
    problemas=Problems.objects.all()

    listaProblemas=[]

    for i in problemas:
        listaProblemas.append((i.problem_name, i.problem_points, i.problem_link))

    return render(request, 'problems.html', {'problemas':listaProblemas})