#Importo librerías
from django.shortcuts import render, redirect
from django.http import HttpResponse
from contest.models import Contest
import json

# Create your views here.

#Constantes
cantidad_problemas=12

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

#Funcion para extraer problemas del JSON del contest
def extraerProblemasDeContest(JSON):
    #Lista de problemas del contest
    listaProblemas=[]
    #Por cada problema extraemos sus datos
    for problema in JSON:
        #Insertamos el problema en la lista
        listaProblemas.append((problema['problem_name'], problema['problem_link'], problema['problem_judge']))
    #Si la lista tiene menos de 12 problemas, rellenamos sin valores
    while(len(listaProblemas)<12):
        #Dejamos los campos vacios
        listaProblemas.append(('','',''))
    #Devolvemos la lista de problemas
    return listaProblemas

#Editar contest
def editContest(request):
    #Si es POST, modificamos los datos y redireccionamos a contestManager
    if request.method=='POST':
        #Nombre original del contest
        contest_name_original=''
        #Si tengo los datos que envía contestManager
        if 'editContest' in request.session:
            #Contest name
            contest_name_original=request.session['editContest']
        #Nombre del contest a modificar
        contest_name=request.POST['contest_name']
        #Duración en minutos del contest a modificar
        contest_length=request.POST['contest_length']
        #Nombres de los problemas del contest a modificar
        problem_names=request.POST.getlist('problem_name')
        #Links de los problemas del contest a modificar
        problem_links=request.POST.getlist('problem_link')
        #Jueces de los problemas del contest a modificar
        problem_judges=request.POST.getlist('Online-Judge')
        #Traigo la lista de contest de la base de datos
        contests=Contest.objects.all()
        #Miro la lista de contest para buscar el que quiero editar
        for contest in contests:
            #Lo paso a JSON
            JSON=json.loads(contest.contest_info)
            #Si coincide con el nombre del contest que se quiere editar
            if JSON['contest_name']==contest_name_original:
                #Cambiamos el nombre del contest
                JSON['contest_name']=contest_name
                #Cambiamos la duración en minutos del contest
                JSON['contest_length']=contest_length
                #Iteramos por cada uno de los cantidad_problemas problemas para actualizar sus datos
                for problema in range(cantidad_problemas):
                    #Actualizamos nombre de problema
                    JSON['problems'][problema]['problem_name']=problem_names[problema]
                    #Actualizamos link de problema
                    JSON['problems'][problema]['problem_link']=problem_links[problema]
                    #Actualizamos juez de problema
                    JSON['problems'][problema]['problem_judge']=problem_judges[problema]
                #Actualizo los datos del contest en la base de datos
                Contest.objects.filter(contest_info=contest.contest_info).update(contest_info=json.dumps(JSON))
                #Dejamos de iterar porque ya editamos el contest
                break
        #Datos de contest actualizado, redirecciono a página de contestManager
        return redirect("/contestManager")

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
                #Ponemos en la lista el nombre del contest
                datosContest.append(JSON['contest_name'])
                #Ponemos en la lista la duración en minutos del contest
                datosContest.append(JSON['contest_length'])
                #Ponemos en la lista los problemas del contest
                datosContest.append(extraerProblemasDeContest(JSON['problems']))
                #Dejamos de iterar porque ya encontramos el contest
                break
    #Render
    return render(request, 'editContest.html', {'contest':datosContest})