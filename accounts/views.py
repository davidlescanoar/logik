from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Account
from logik.tasks import validarCuentaCodeforces, validarCuentaOIAJ
import datetime 
from datetime import timedelta

#Variables globales
validar=0

# Create your views here.
def accounts(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    global validar

    if request.method=='POST':
        CF_Handle_Input=request.POST['CF_Handle']

        OIAJ_Handle_Input=request.POST['OIAJ_Handle']

        #Fecha y hora actual
        fechaNow=datetime.datetime.now()

        #Asíncrono para validar las cuentas
        validarCuentaCodeforces.apply_async((CF_Handle_Input, request.user.id, request.user.username, fechaNow), countdown=360)
        validarCuentaOIAJ.apply_async((OIAJ_Handle_Input, request.user.id, request.user.username, fechaNow), countdown=361)

        validar=1

        return redirect("/accounts")

    cuenta=Account.objects.filter(AccountID=request.user.id)

    validarCpy=validar

    validar=0

    if cuenta:
        return render(request, "accounts.html", {'cuenta': cuenta[0], 'validar':validarCpy}) 

    return render(request, "accounts.html", {'validar':validarCpy})