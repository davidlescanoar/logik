from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login

from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse
from accounts.models import Account
from django.contrib.auth.models import User

# Create your views here.

def welcome(request):
    if request.user.is_authenticated:
        #De momento, arrancamos en la vista de problemas
        #return render(request, "welcome.html")
        return redirect('/problems')

    return redirect('/login')

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)

                #De momento, arrancamos en la vista de problemas
                return redirect('/problems')

    return render(request, "register.html", {'form': form, 'no_logik_form':1})

def login(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                #De momento, arrancamos en la vista de problemas
                return redirect('/problems')

    return render(request, "login.html", {'form': form, 'no_logik_form':1})

def logout(request):
    do_logout(request)

    return redirect('/')

def usersBulkInsert(request):    
    usersList=[ "unlam_01", "GastonFontenla", "CassCives", "byTomys", "NicoCulini", "ignaciocanta", "OctavioBenjamin", "ivan1214", "LucasTarche", "Federico", "kimberly", "dinamarko", "LeanScher", "OcaranzaJuan", "agustin_rubil", "Fabrizio134", "maxwellcito", "JoacruYT", "Agus", "dariotzvir", "Octaa1", "Fahuel", "FacuRamirez", "SirDella", "HelcsnewsXD", "Yamil", "test.prueba", "NahuelMenendez", "Villagran", "franco", "NicolasGiglio", "GonzaloSilvero", "PabloPa", "IbanElTrolazo", "MatiBusta", "Andre", "Fran", "aguss.reinoso", "Michaella1602", "DiegoLopez", "nmbenitez", "ValenPiris", "AlisonMadero", "Gonzalo_Ortiz", "Ayrton", "rolondanico", "AngelFontenla", "Uli7", "lourdes_04", "AgussReinoso", "bcena", "AguusLopez50", "Dylan", "rodrigomaidana", "MauricioMn43", "Facundo", "IgnacioFlaks", "Nico_626", "FrancoM", "Emilianopat", "Alex", "Nicolas", "Nahuelfl", "FeerFl", "lourdes", "NicolasWalsh", "Iglesiassanti", "RamiroPalacios", "LautaroSolano", "magalilucia1", "ailinm", "alansio", "julicapo100", "lazaro", "Alan", "EzequielMedolla", "Luli_Lavayen", "LeonardoTorres", "MatiasPereira", "SantiagoGomez", "aagusfernandez0", "LeonelGutierrez", "43316397", "maury", "FranchitoMovil", "Malena", "fernando", "damiante", "ariloc", "DanielMunoz", "Marcio.r", "Maximodbritez", "ledesma_leandro", "PedroOcaranza", "UnaPlanta", "dario dosci", "Daxger", "matias", "Nahuel", "Medinaadrian", "AlejoAseijas", "EzequielVeron" ]

    UserAccountID=100

    s=""

    for user in usersList:
        if not Account.objects.filter(Logik_Handle=user).exists():
            Account.objects.create(AccountID=UserAccountID, Logik_Handle=user, OIAJ_Handle=user)

            UserAccountID+=1

        if not User.objects.filter(username=user).exists():
            User.objects.create(username=user)

    users=User.objects.all()

    for user in users:
        s+=str(user)+" "

    return HttpResponse('<h1>'+s+'</h1>')