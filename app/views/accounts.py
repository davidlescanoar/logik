from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.models import Account
from logik.tasks import validarCuentas
import datetime
from datetime import timedelta
from celery import group


# Create your views here.
def accounts(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':
        CF_Handle_Input = request.POST['CF_Handle']
        OIAJ_Handle_Input = request.POST['OIAJ_Handle']
        CSES_Handle_Input = request.POST['CSES_Handle']
        SPOJ_Handle_Input = request.POST['SPOJ_Handle']
        OnlineJudge_Handle_Input = request.POST['OnlineJudge_Handle']

        # Fecha y hora actual
        fechaNow = int(datetime.datetime.now().timestamp())

        # Asíncrono para validar las cuentas
        validarCuentas.apply_async(
            (
                fechaNow,
                CF_Handle_Input,
                OIAJ_Handle_Input,
                CSES_Handle_Input,
                SPOJ_Handle_Input,
                OnlineJudge_Handle_Input,
                request.user.id,
                request.user.username,
            ),
            countdown=30
        )

        request.session['validar'] = 1

        return redirect("/accounts")

    cuenta = Account.objects.filter(AccountID=request.user.id)

    validar = 0

    if 'validar' in request.session and request.session.get('validar', 1):
        validar = 1

    request.session['validar'] = 0

    if cuenta:
        return render(request, "accounts.html", {'cuenta': cuenta[0], 'validar': validar})

    return render(request, "accounts.html", {'validar': validar})
