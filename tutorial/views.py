from django.shortcuts import render,redirect
from django.http import HttpResponse
from tutorial.models import Tutorial

# Create your views here.
def tutorial(request):
    #Si no está autenticado, no puede entrar
    if not request.user.is_authenticated:
        return redirect('/login')
    #Tutoriales
    tutoriales=Tutorial.objects.all()
    #Diccionario en donde guardo los datos de los tutoriales
    data={}
    #Por cada tutorial
    for tuto in tutoriales:
        #Creo la lista para agregar los datos
        data[tuto.id_tutorial]=[tuto.titulo,tuto.descripcion,tuto.autor,tuto.cuerpo,tuto.likes,tuto.comentarios]
    #Renderizo
    return render(request,'tutorial.html',{'tutorialData':data})

#Leer tutorial
def leerTutorial(request,id_tutorial):
    #Si no está autenticado, no puede entrar
    if not request.user.is_authenticated:
        return redirect('/login')
    #Si el tutorial existe, lo recupero y lo renderizo
    if Tutorial.objects.filter(id_tutorial=id_tutorial):
        return render(request,'viewTutorial.html',{'tutorialData':Tutorial.objects.get(id_tutorial=id_tutorial)})
    #No existe, vuelvo a la página de los tutoriales
    return redirect('/tutorial')