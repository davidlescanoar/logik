from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Account
from logik.tasks import validarCuentaCodeforces, validarCuentaOIAJ, actualizarCuentaCSES
import datetime 
from datetime import timedelta

# Create your views here.
def accounts(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method=='POST':
        CF_Handle_Input=request.POST['CF_Handle']

        OIAJ_Handle_Input=request.POST['OIAJ_Handle']

        CSES_Handle_Input=request.POST['CSES_Handle']

        #Fecha y hora actual
        fechaNow=datetime.datetime.now()

        #Asíncrono para validar las cuentas
        validarCuentaCodeforces.apply_async((CF_Handle_Input, request.user.id, request.user.username, fechaNow), countdown=360)
        validarCuentaOIAJ.apply_async((OIAJ_Handle_Input, request.user.id, request.user.username, fechaNow), countdown=361)
        actualizarCuentaCSES.apply_async((CSES_Handle_Input, request.user.id, request.user.username, fechaNow), countdown=362)

        request.session['validar']=1

        return redirect("/accounts")

    cuenta=Account.objects.filter(AccountID=request.user.id)

    validar=0

    if 'validar' in request.session and  request.session.get('validar', 1):
        validar=1

    request.session['validar']=0

    if cuenta:
        return render(request, "accounts.html", {'cuenta': cuenta[0], 'validar':validar}) 

    return render(request, "accounts.html", {'validar':validar})