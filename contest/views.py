#Importo librerías
from django.shortcuts import render, redirect
from django.http import HttpResponse
from contest.models import Contest
import json

# Create your views here.

#Vista de contest
def contest(request):
    return render(request, 'contests.html')

#Eliminar contest
def eliminarContest(contest_name):
    #Lista con contests a eliminar (si varios tienen el mismo nombre borra todos)
    contests=Contest.objects.all()
    #Miro cada contest
    for contest in contests:
        #Transformo a JSON
        JSON=json.loads(contest.contest_info)
        #Si coincide con el nombre lo tengo que eliminar
        if JSON['contest_name']==contest_name:
            #Lo elimino
            Contest.objects.filter(contest_info=contest.contest_info).delete()
    
#Vista de contest manager
def contestManager(request):    
    #Si se quiere realizar una acción (editar/eliminar)
    if request.method=='POST':
        #Se quiere editar el contest
        if 'editar' in request.POST:
            #Guardamos datos en el request de que se quiere editar
            request.session['editContest']=request.POST['editar']
            #Cargamos página para editar datos del contest
            return redirect('/editContest')
        #Se quiere eliminar el contest
        if 'eliminar' in request.POST:
            #Eliminamos los contest que coincidan con el nombre seleccionado
            eliminarContest(request.POST['eliminar'])
        #Recargamos página
        return redirect("/contestManager")

    #Lista de contest
    contests=[]
    #Contest de la DB
    listaContest=Contest.objects.all()
    #Miro la información de cada contest (en JSON)
    for contest in listaContest:
        #Lo paso a JSON
        JSON=json.loads(contest.contest_info)
        #Agrego la info del contest a contests
        contests.append((JSON['contest_name'], JSON['contest_length']))
    #Render
    return render(request, 'contestManager.html', {'contests':contests})

#Editar contest
def editContest(request):
    #Parámetros a pasarle al html
    datosContest=[]
    #Si tengo los datos que envía contestManager
    if 'editContest' in request.session:
        #Contest name
        contest_name=request.session['editContest']
        #Traigo todos los contest y despus filtro
        contests=Contest.objects.all()
        #Recorro todos los contest
        for contest in contests:
            #Lo paso a JSON
            JSON=json.loads(contest.contest_info)
            #Si coincide con el nombre del contest que se quiere editar
            if JSON['contest_name']==contest_name:
                #Pasamos los datos a 'datosContest'
                datosContest=(JSON['contest_name'], JSON['contest_length'])
                #Dejamos de iterar porque ya encontramos el contest
                break
    #Render
    return render(request, 'editContest.html', {'contest':datosContest})